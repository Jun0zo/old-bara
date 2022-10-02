from pydantic import BaseModel, EmailStr, validator


class UserRoleCreate(BaseModel):
    name: str


class UserRoleUpdate(BaseModel):
    name: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserUpdate(BaseModel):
    current_password: str = None
    new_password: str = None
    new_password_check: str = None
    name: str = None
    role_id: int = None
    plate_fee: int = None
    contract_fee: float = None
    permission_user: str = None
    permission_transaction: str = None
    permission_invoice: str = None

    @validator("permission_user")
    def validate_permission_user(cls, val):
        available_list = ["SR", "AR", "ARW"]
        if val not in available_list:
            raise ValueError(f"permission_user은(는) {available_list}중 하나여야 합니다.")
        return val

    @validator("permission_transaction")
    def validate_permission_transaction(cls, val):
        available_list = ["SRW", "AR", "ARW"]
        if val not in available_list:
            raise ValueError(f"permission_transaction은(는) {available_list}중 하나여야 합니다.")
        return val

    @validator("permission_invoice")
    def validate_permission_invoice(cls, val):
        available_list = ["SR", "AR", "ARW"]
        if val not in available_list:
            raise ValueError(f"permission_invoice은(는) {available_list}중 하나여야 합니다.")
        return val


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ResetPassword(BaseModel):
    token: str
    new_password: str
    new_password_check: str


class InsuranceCompanyCreate(BaseModel):
    name: str


class InsuranceCompanyUpdate(BaseModel):
    name: str


class TransactionCreate(BaseModel):
    user_id: int = None
    insurance_company_id: int
    vehicle_id: str
    vehicle_model: str
    date: str
    price: int
    memo: str = None


class TransactionTable(BaseModel):
    start_date: str = None
    end_date: str = None
    user_id: str = None
    insurance_company_id: int = None
    page: int = 0
    limit: int = 15
    canceled_type: str = "ALL"
    order_by: str = "transaction_id"
    order_type: str = "desc"

    @validator("canceled_type")
    def validate_canceled_type(cls, val):
        available_list = ["ALL", "EXCLUDE_CANCELED", "CANCELED_ONLY"]
        if val not in available_list:
            raise ValueError(f"canceled_type은(는) {available_list}중 하나여야 합니다.")
        return val

    @validator("order_by")
    def validate_order_by(cls, val):
        available_list = ["transaction_id", "user_id", "price", "cancel_fee"]
        if val not in available_list:
            raise ValueError(f"order_by은(는) {available_list}중 하나여야 합니다.")
        return val

    @validator("order_type")
    def validate_order_type(cls, val):
        available_list = ["desc", "asc"]
        if val not in available_list:
            raise ValueError(f"order_type은(는) {available_list}중 하나여야 합니다.")
        return val


class TransactionUpdate(BaseModel):
    user_id: int = None
    insurance_company_id: int = None
    vehicle_id: str = None
    vehicle_model: str = None
    date: str = None
    price: int = None
    memo: str = None
    canceled: bool = None
    cancel_fee: int = None


class UserInvoiceCreate(BaseModel):
    user_id: int
    year: str
    month: str


class UserInvoiceExtraCreate(BaseModel):
    user_id: int
    year: str
    month: str
    name: str
    price: int


class UserInvoiceExtraUpdate(BaseModel):
    name: str
    price: int


class CompanyInvoiceCreate(BaseModel):
    year: str
    month: str
    rental_fee: int
    maintenance_fee: int


class CompanyInvoiceExtraCreate(BaseModel):
    year: str
    month: str
    name: str
    price: int


class CompanyInvoiceExtraUpdate(BaseModel):
    name: str
    price: int
