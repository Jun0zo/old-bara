from datetime import datetime
from pytz import timezone
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Session

from app.database.conn import Base, db


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        setattr(obj, "created_at", datetime.now(timezone("Asia/Seoul")))
        setattr(obj, "updated_at", datetime.now(timezone("Asia/Seoul")))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, with_entities: list = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)
        if with_entities:
            query = query.with_entities(*with_entities)
        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        if not session:
            sess.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, with_entities: list = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == "gt":
                cond.append((col > val))
            elif len(key) == 2 and key[1] == "gte":
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == "lt":
                cond.append((col < val))
            elif len(key) == 2 and key[1] == "lte":
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == "in":
                cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        if with_entities:
            query = query.with_entities(*with_entities)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, auto_commit: bool = False, **kwargs):
        kwargs["updated_at"] = datetime.now(timezone("Asia/Seoul"))
        qs = self._q.update(kwargs)
        ret = None

        self._session.flush()
        if qs > 0:
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


class UserRole(Base, BaseMixin):
    __tablename__ = "user_role"
    name = Column(String(length=10), nullable=False, unique=True)


class Permission(Base, BaseMixin):
    __tablename__ = "permission"
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = Column(Enum("SR", "AR", "ARW"), default="SR")
    transaction = Column(Enum("SRW", "AR", "ARW"), default="SRW")
    invoice = Column(Enum("SR", "AR", "ARW"), default="SR")
    """
        SR = Self Read(본인 user.id에 대한 조회만 가능)
        SRW = Self Read(본인 user.id에 대한 CRUD 가능)
        AR = All Read(모든 user.id에 대한 조회만 가능)
        ARW = All Read and Write(모든 user.id에 대한 CRUD 가능)
    """


class User(Base, BaseMixin):
    __tablename__ = "user"
    email = Column(String(length=255), nullable=False, unique=True)
    email_token = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=255), nullable=False, unique=True)
    name = Column(String(length=10), nullable=False)
    role_id = Column(Integer, ForeignKey("user_role.id"))
    status = Column(Enum("registered", "verified", "accepted", "deleted"), default="registered")
    plate_fee = Column(Integer, default=0)
    contract_fee = Column(Float, default=0.0)


class InsuranceCompany(Base, BaseMixin):
    __tablename__ = "insurance_company"
    name = Column(String(length=10), nullable=False, unique=True)


class Transaction(Base, BaseMixin):
    __tablename__ = "transaction"
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    insurance_company_id = Column(Integer, ForeignKey("insurance_company.id"), nullable=False)
    vehicle_id = Column(String(length=10), nullable=False)
    vehicle_model = Column(String(length=10), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    memo = Column(String(length=10), nullable=False)
    canceled = Column(Boolean, default=False)
    cancel_fee = Column(Integer, default=0)


class UserInvoice(Base, BaseMixin):
    __tablename__ = "user_invoice"
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    contract_fee = Column(Float, nullable=False)  # 수수료 퍼센트(e.g. 15)
    plate_fee = Column(Integer, nullable=False)  # 지입료(e.g. 220000)
    year = Column(Integer, nullable=False)  # 연도 (e.g. 2022)
    month = Column(Integer, nullable=False)  # 월 (e.g. 6)
    transaction_count = Column(Integer, nullable=False)  # 취소 건 포함 총 transaction 개수
    canceled_transaction_count = Column(Integer, nullable=False)  # 취소 건 개수
    revenue = Column(Integer, nullable=False)  # 취소 수수료 제외 매출
    cancel_fee = Column(Integer, nullable=False)  # 취소 수수표 합계
    total_revenue = Column(Integer, nullable=False)  # 취소 수수료 포함 총 매출
    total_contract_fee = Column(Integer, nullable=False)  # 수수료 합계
    first_vat = Column(Integer, nullable=False)  # 1차 부가세
    first_income = Column(Integer, nullable=False)  # 1차 순이익
    second_vat = Column(Integer, default=0)  # 2차 부가세
    second_income = Column(Integer, default=0)  # 2차 순이익
    income = Column(Integer, nullable=False)  # 최종 순이익


class UserInvoiceExtra(Base, BaseMixin):
    __tablename__ = "user_invoice_extra"
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    name = Column(String(length=15), nullable=False)
    price = Column(Integer, nullable=False)


class CompanyInvoice(Base, BaseMixin):
    __tablename__ = "company_invoice"
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    revenue = Column(Integer, nullable=False)  # 모든 직원의 매출 합계(취소 수수료 포함)
    plate_fee = Column(Integer, nullable=False)  # 모든 직원의 지입료 합계
    employee_salary = Column(Integer, nullable=False)  # 모든 직원의 급여 합계
    rental_fee = Column(Integer, nullable=False)  # 사무실 임대료
    maintenance_fee = Column(Integer, nullable=False)  # 사무실 관리비
    income = Column(Integer, nullable=False)  # 회사 순수익


class CompanyInvoiceExtra(Base, BaseMixin):
    __tablename__ = "company_invoice_extra"
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    name = Column(String(length=15), nullable=False)
    price = Column(Integer, nullable=False)
