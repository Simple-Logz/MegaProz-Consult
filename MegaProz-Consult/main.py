from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.database import engine, Base
from app.config import settings
from app.routers import auth, surveys, formations, samples

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="MegaProz-Consult",
    description="Hello I need you to help me generate a set of code. But I can use to deploy. A web application. That can be used to deliver geological services such as. Borehole drilling, Soak away drilling, Soil testing. Industrial cleaning. Cons Con Geological Consultations. Erosion control, etcetera. Give me a stack of codes, very simple ones that I can use to just deploy the application and ensure that. This set of codes are validated and error proof. Make sure that the codes that you give me are enough for me to readily deploy my application. The name of the site will be MegaProz Consult. ank you.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(auth.router, prefix="/api/v1")
app.include_router(surveys.router, prefix="/api/v1")
app.include_router(formations.router, prefix="/api/v1")
app.include_router(samples.router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "MegaProz-Consult", "version": "1.0.0"}