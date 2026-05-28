from flask import Blueprint, abort, current_app, jsonify, render_template


docs_bp = Blueprint("docs", __name__)


def ensure_development() -> None:
    if current_app.config["ENV_NAME"] != "development":
        abort(404)


@docs_bp.get("")
@docs_bp.get("/")
def swagger_ui():
    ensure_development()

    return render_template("docs.html")


@docs_bp.get("/openapi.json")
def openapi_json():
    ensure_development()

    base_url = current_app.config["BASE_URL"].rstrip("/")
    sample_id = "6f2f0139-eed8-4da8-ae78-9674e10b3f5e"

    return jsonify(
        {
            "openapi": "3.0.3",
            "info": {
                "title": "Ragnarok Coupons API",
                "version": "1.0.0",
                "description": "API simples de importacao e resgate unico de cupons.",
            },
            "servers": [{"url": base_url}],
            "components": {
                "securitySchemes": {
                    "ApiKeyAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "api-key",
                    }
                },
                "schemas": {
                    "FailedResponse": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "failed"},
                            "message": {"type": "string", "example": "already used"},
                        },
                    }
                },
            },
            "paths": {
                "/health/": {
                    "get": {
                        "summary": "Health check",
                        "responses": {
                            "200": {
                                "description": "API e MongoDB respondendo",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {"type": "string", "example": "ok"},
                                                "database": {"type": "string", "example": "ragnarok"},
                                            },
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/api/genragcode": {
                    "get": {
                        "summary": "Gerar URL de resgate",
                        "security": [{"ApiKeyAuth": []}],
                        "responses": {
                            "200": {
                                "description": "URL de resgate gerada",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "url": {
                                                    "type": "string",
                                                    "example": f"{base_url}/pages/{sample_id}",
                                                }
                                            },
                                        }
                                    }
                                },
                            },
                            "401": {
                                "description": "API key invalida",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/FailedResponse"}
                                    }
                                },
                            },
                            "404": {
                                "description": "Nenhum cupom valido disponivel",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/FailedResponse"}
                                    }
                                },
                            },
                        },
                    }
                },
                "/api/import/codes": {
                    "post": {
                        "summary": "Importar CSV de cupons",
                        "security": [{"ApiKeyAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["csv"],
                                        "properties": {
                                            "csv": {
                                                "type": "string",
                                                "format": "binary",
                                            }
                                        },
                                    }
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Cupons importados",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {
                                                    "type": "string",
                                                    "example": "success",
                                                },
                                                "inserted": {
                                                    "type": "integer",
                                                    "example": 10,
                                                },
                                            },
                                        }
                                    }
                                },
                            },
                            "400": {
                                "description": "CSV invalido",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/FailedResponse"}
                                    }
                                },
                            },
                            "401": {
                                "description": "API key invalida",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/FailedResponse"}
                                    }
                                },
                            },
                        },
                    }
                },
                "/api/{coupon_id}": {
                    "get": {
                        "summary": "Resgatar cupom",
                        "parameters": [
                            {
                                "name": "coupon_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "string", "format": "uuid"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Cupom resgatado",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {
                                                    "type": "string",
                                                    "example": "success",
                                                },
                                                "code": {
                                                    "type": "string",
                                                    "example": "RAGNAROK-001",
                                                },
                                            },
                                        }
                                    }
                                },
                            },
                            "400": {
                                "description": "UUID invalido",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/FailedResponse"}
                                    }
                                },
                            },
                            "409": {
                                "description": "Cupom ja usado ou nao encontrado",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/FailedResponse"}
                                    }
                                },
                            },
                        },
                    }
                },
                "/pages/{coupon_id}": {
                    "get": {
                        "summary": "Abrir pagina de resgate",
                        "parameters": [
                            {
                                "name": "coupon_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "string", "format": "uuid"},
                            }
                        ],
                        "responses": {
                            "200": {"description": "Pagina HTML de resgate"},
                            "400": {"description": "UUID invalido"},
                        },
                    }
                },
                "/pages/demo": {
                    "get": {
                        "summary": "Pagina de demonstracao",
                        "description": "Disponivel apenas com FLASK_ENV=development.",
                        "responses": {
                            "200": {"description": "Pagina HTML de demonstracao"},
                            "404": {"description": "Indisponivel fora de development"},
                        },
                    }
                },
                "/docs": {
                    "get": {
                        "summary": "Swagger UI",
                        "description": "Disponivel apenas com FLASK_ENV=development.",
                        "responses": {
                            "200": {"description": "Swagger UI"},
                            "404": {"description": "Indisponivel fora de development"},
                        },
                    }
                },
            },
        }
    )
