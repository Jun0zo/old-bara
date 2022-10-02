from dataclasses import asdict
from os import path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.common.config import conf
from app.database.conn import db, Base
from app.routes import dashboard, invoice, transaction, user
from app.utils.create_dummy_data import create_dummy_data
from app.utils.create_superuser import create_superuser


conf_dict = asdict(conf())
app = FastAPI(docs_url=conf_dict["SWAGGER_URL"], redoc_url=conf_dict["REDOC_URL"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=conf_dict["ALLOW_SITE"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dashboard.router, tags=["Dashboard"], prefix="/api")
app.include_router(invoice.router, tags=["Invoice"], prefix="/api")
app.include_router(transaction.router, tags=["Transaction"], prefix="/api")
app.include_router(user.router, tags=["User"], prefix="/api")
app.mount("/build", StaticFiles(directory=path.join(conf_dict["BASE_DIR"], "app", "templates", "build")), name="build")
app.mount(
    "/static", StaticFiles(directory=path.join(conf_dict["BASE_DIR"], "app", "templates", "static")), name="static"
)


@app.get("/{full_path:path}")
async def render_spa(full_path: str):
    index_html_path = path.join(conf_dict["BASE_DIR"], "app", "templates", "index.html")

    with open(index_html_path, "rt", encoding="UTF-8") as f:
        index_html = f.read()

    return HTMLResponse(content=index_html, status_code=200)


db.init_app(app, **conf_dict)

# local env
if __name__ == "__main__":
    is_use_dummy_data = False
    is_create_dummy_data = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "--use-dummy-data":
            is_use_dummy_data = True
        elif sys.argv[1] == "--create-dummy-data":
            is_create_dummy_data = True

    if is_create_dummy_data:
        Base.metadata.create_all(db.engine)
        session = next(db.session())
        print("Dummy data 생성으로 인해 서버 구동까지 약 1~3분 소요됩니다.")
        create_dummy_data(db)

    else:
        if not is_use_dummy_data:
            Base.metadata.create_all(db.engine)
            session = next(db.session())
            metadata = Base.metadata
            except_tables = []

            # Clear table
            session.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for table in metadata.sorted_tables:
                if table.name not in except_tables:
                    session.execute(table.delete())
            session.execute("SET FOREIGN_KEY_CHECKS = 1;")
            session.commit()
            session = next(db.session())

            # Create Superuser
            create_superuser(session)

    # Run uvicorn
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=[path.join(conf_dict["BASE_DIR"], "app")]
    )
