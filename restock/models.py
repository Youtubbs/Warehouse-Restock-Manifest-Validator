from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["electronics", "perishable", "apparel", "hardware"]


class RestockItem(BaseModel):
    """A single validated row of a warehouse restock manifest."""

    sku: str
    warehouse: str
    quantity: int = Field(gt=0)
    unit_cost: float = Field(gt=0)
    category: Category

    @property
    def line_total(self) -> float:
        return self.quantity * self.unit_cost
