from datetime import datetime, timedelta
from random import choice, randint, uniform
from uuid import uuid4

import bcrypt

from app.database.conn import SQLAlchemy
from app.database.schema import (
    CompanyInvoice,
    CompanyInvoiceExtra,
    InsuranceCompany,
    Transaction,
    User,
    UserInvoice,
    UserInvoiceExtra,
    UserRole,
    Permission,
)
from app.routes.invoice import calculate_company_invoice, calculate_user_invoice
from app.utils.create_superuser import create_superuser


def create_dummy_data(db: SQLAlchemy) -> None:
    company_names = ["애니카", "현대해상", "제휴사"]
    user_names = ["김제니", "박채영", "김지수", "라리사"]
    user_emails = ["jennie@blackpink.com", "chaeyoung@blackpink.com", "jisoo@blackpink.com", "lalisa@blackpink.com"]
    korean = ["가", "나", "다", "라", "마", "바", "사"]
    car_names = ["아반떼", "소나타", "그랜져", "제네시스", "K3", "K5", "K7", "K9", "벤츠 E220d", "벤츠 S500", "람보르기니 우라칸", "부가티 시론"]
    memos = ["" for _ in range(28)]
    memos.extend(["메모1", "메모2"])
    user_invoice_extra = ["" for _ in range(4)]
    user_invoice_extra.extend(["명절 보너스"])
    company_invoice_extra = ["" for _ in range(3)]
    company_invoice_extra.extend([("추가 지출", randint(-100, -50) * 10000), ("추가 수입", randint(50, 100) * 10000)])
    password = "testpassword1!"

    session = next(db.session())
    create_superuser(session)

    for name in company_names:
        InsuranceCompany.create(session=session, auto_commit=True, name=name)

    UserRole.create(session=session, auto_commit=True, name="기사")

    for i in range(len(user_names)):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        User.create(
            session=session,
            auto_commit=True,
            email=user_emails[i],
            email_token=uuid4().hex,
            password=hashed_password,
            name=user_names[i],
            role_id=UserRole.get(session=session, name="기사").id,
            status="accepted",
            plate_fee=randint(15, 20) * 10000,
            contract_fee=round(uniform(15, 20), 1),
        )
        Permission.create(
            session=session,
            auto_commit=True,
            user_id=User.get(session=session, email=user_emails[i]).id,
            user="SR",
            transaction="SRW",
            invoice="SR",
        )

        for _ in range(randint(500, 1000)):
            canceled = False
            cancel_fee = 0

            if randint(1, 20) == 1:
                canceled = True
                cancel_fee = (randint(5, 15) * 1000,)

            Transaction.create(
                session=session,
                auto_commit=True,
                user_id=User.get(session=session, email=user_emails[i]).id,
                insurance_company_id=InsuranceCompany.get(session=session, name=choice(company_names)).id,
                vehicle_id=str(randint(10, 150)) + choice(korean) + " " + str(randint(1000, 9999)),
                vehicle_model=choice(car_names),
                date=(datetime(2022, 1, 1) + timedelta(days=randint(0, 180))).strftime("%Y-%m-%d"),
                price=randint(100, 250) * 1000,
                memo=choice(memos),
                canceled=canceled,
                cancel_fee=cancel_fee,
            )

        for month in range(1, 6):
            extra = choice(user_invoice_extra)
            user = User.get(session=session, email=user_emails[i])

            if extra:
                UserInvoiceExtra.create(
                    session=session,
                    auto_commit=True,
                    user_id=user.id,
                    year=2022,
                    month=month,
                    name=extra,
                    price=randint(100, 250) * 1000,
                )

            to_create = calculate_user_invoice(
                user=user,
                user_id=user.id,
                year=2022,
                month=month,
                session=session,
            )
            del to_create["extra"]
            UserInvoice.create(session=session, auto_commit=True, **to_create)

    for month in range(1, 6):
        extra = choice(company_invoice_extra)
        user = User.get(session=session, email=user_emails[i])

        if extra:
            CompanyInvoiceExtra.create(
                session=session,
                auto_commit=True,
                year=2022,
                month=month,
                name=extra[0],
                price=extra[1],
            )

        to_create = calculate_company_invoice(
            year=2022,
            month=month,
            rental_fee=randint(50, 100) * 10000,
            maintenance_fee=randint(5, 10) * 10000,
            session=session,
        )
        del to_create["extra"]
        CompanyInvoice.create(session=session, auto_commit=True, **to_create)
