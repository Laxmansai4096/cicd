"""
Data Models & Schemas for Retail Pricing & Checkout Engine
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class CartItem(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit code", example="SKU-HDPH-01")
    name: str = Field(..., description="Product display name", example="UltraNoise Pro Wireless Headphones")
    price: float = Field(..., gt=0, description="Unit retail price", example=249.99)
    quantity: int = Field(..., gt=0, description="Quantity to purchase", example=2)

class CheckoutRequest(BaseModel):
    items: List[CartItem] = Field(..., description="List of items in the shopping cart")
    promo_code: Optional[str] = Field(default="", description="Promotional coupon code (e.g. WELCOME10, VIP20, FLASH50)")
    state: Optional[str] = Field(default="TX", description="2-letter US State code for sales tax calculation", example="TX")

class CheckoutResponse(BaseModel):
    subtotal: float
    bulk_savings: float
    promo_savings: float
    total_savings: float
    taxable_amount: float
    sales_tax: float
    final_total: float
    state: str
    item_count: int

class PromoValidationRequest(BaseModel):
    promo_code: str

class PromoValidationResponse(BaseModel):
    promo_code: str
    is_valid: bool
    discount_percentage: float
    description: str
