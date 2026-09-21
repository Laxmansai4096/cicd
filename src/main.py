"""
Retail Checkout & Calculation Microservice API
FastAPI application powering cart totals, promo discounts, and multi-state tax.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.models import (
    CheckoutRequest,
    CheckoutResponse,
    PromoValidationRequest,
    PromoValidationResponse
)
from src.retail_calc import (
    calculate_final_total,
    VALID_PROMO_CODES
)

app = FastAPI(
    title="Retail Hub Pricing Engine API",
    description="Enterprise microservice for checkout calculations, promotional tiers, and multi-state taxes.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Sample Catalog (used for product lookup)
PRODUCT_CATALOG = {
    "SKU-HDPH-01": {"sku": "SKU-HDPH-01", "name": "UltraNoise Pro Wireless Headphones", "price": 249.99, "category": "Audio"},
    "SKU-LAPTOP-X1": {"sku": "SKU-LAPTOP-X1", "name": "ApexBlade 16 Gaming Laptop", "price": 1899.99, "category": "Computers"},
    "SKU-CHRG-02": {"sku": "SKU-CHRG-02", "name": "FastCharge 65W GaN USB-C Charger", "price": 39.99, "category": "Accessories"},
    "SKU-MOUSE-03": {"sku": "SKU-MOUSE-03", "name": "PrecisionFlow Wireless Ergonomic Mouse", "price": 79.99, "category": "Accessories"}
}

@app.get("/", tags=["General"])
def root_info():
    """Service landing page and metadata."""
    return {
        "service": "Retail Hub Pricing Engine",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Kubernetes / Azure Container Apps liveness and readiness probe."""
    return {
        "status": "healthy",
        "service": "retail-pricing-engine",
        "version": "1.0.0"
    }

@app.get("/api/v1/catalog", tags=["Catalog"])
def get_catalog():
    """Retrieve full product catalog with current retail prices."""
    return {
        "status": "success",
        "count": len(PRODUCT_CATALOG),
        "products": list(PRODUCT_CATALOG.values())
    }

@app.post("/api/v1/promos/validate", response_model=PromoValidationResponse, tags=["Promotions"])
def validate_promo_code(payload: PromoValidationRequest):
    """Check if a promotional coupon code is valid and return discount details."""
    code = payload.promo_code.strip().upper()
    if code in VALID_PROMO_CODES:
        rate = VALID_PROMO_CODES[code]
        return PromoValidationResponse(
            promo_code=code,
            is_valid=True,
            discount_percentage=rate * 100.0,
            description=f"Valid coupon: {int(rate * 100)}% off cart subtotal"
        )
    return PromoValidationResponse(
        promo_code=payload.promo_code,
        is_valid=False,
        discount_percentage=0.0,
        description="Invalid or expired promo code"
    )

@app.post("/api/v1/checkout", response_model=CheckoutResponse, tags=["Checkout"])
def calculate_checkout(payload: CheckoutRequest):
    """
    Calculate full itemized invoice including subtotal, bulk discounts,
    promotional coupons, and destination sales tax.
    """
    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot checkout with an empty cart. Please add at least one item."
        )
    
    # Convert Pydantic items to dictionaries for calculation engine
    items_dicts = [item.model_dump() for item in payload.items]
    invoice = calculate_final_total(
        items=items_dicts,
        promo_code=payload.promo_code or "",
        state=payload.state or "TX"
    )
    
    total_items_count = sum(item.quantity for item in payload.items)
    
    return CheckoutResponse(
        subtotal=invoice["subtotal"],
        bulk_savings=invoice["bulk_savings"],
        promo_savings=invoice["promo_savings"],
        total_savings=invoice["total_savings"],
        taxable_amount=invoice["taxable_amount"],
        sales_tax=invoice["sales_tax"],
        final_total=invoice["final_total"],
        state=invoice["state"],
        item_count=total_items_count
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
