from copy import deepcopy

DEFAULT_RESPONSES = {
    200: {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {"application/json": {"example": {"success": True, "message": "OK"}}},
    },
    201: {
        "description": "요청 리소스가 성공적으로 생성되었을 경우",
        "content": {
            "application/json": {"example": {"success": True, "message": "OK", "result": {"created_object_id": 1}}}
        },
    },
    400: {
        "description": "요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우",
        "content": {"application/json": {"example": {"success": False, "message": "비밀번호는 8자 이상, 20자 이하여야 합니다!"}}},
    },
    401: {
        "description": "Token이 유효하지 않은 경우",
        "content": {"application/json": {"example": {"detail": "Token expired"}}},
    },
    403: {
        "description": "Token이 없거나 권한이 부족한 경우",
        "content": {"application/json": {"example": {"success": False, "message": "권한이 없습니다!"}}},
    },
    409: {
        "description": "DB, 메일 전송 오류 등 예상치 못한 오류가 발생한 경우",
        "content": {"application/json": {"example": {"success": False, "message": "예상치 못한 오류가 발생했습니다!"}}},
    },
    422: {
        "description": "요청 파라미터가 유효하지 않은 경우",
        "content": {
            "application/json": {
                "example": {
                    "detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]
                }
            }
        },
    },
}


def create_role_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_all_role_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": [{"id": 1, "name": "대표"}, {"id": 2, "name": "전무"}],
                }
            }
        },
    }
    return result


def get_specific_role_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"id": 1, "name": "대표"},
                }
            }
        },
    }
    return result


def update_role_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def delete_role_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"deleted_object_id": 1},
                }
            }
        },
    }
    return result


def create_user_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200, 401, 403]
    for key in to_delete:
        del result[key]
    return result


def get_all_user_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": [
                        {
                            "id": 1,
                            "email": "admin@baraman.kr",
                            "name": "홍길동",
                            "role_id": 2,
                            "role_name": "대표",
                            "status": "accepted",
                            "plate_fee": 1234,
                            "contract_fee": 12.34,
                            "permission_user": "ARW",
                            "permission_transaction": "ARW",
                            "permission_invoice": "ARW",
                        },
                        {
                            "id": 2,
                            "email": "useruser@naver.com",
                            "name": "김태원",
                            "status": "verified",
                        },
                    ],
                }
            }
        },
    }
    return result


def get_specific_user_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "id": 1,
                        "email": "admin@baraman.kr",
                        "name": "홍길동",
                        "role_id": 2,
                        "role_name": "대표",
                        "status": "accepted",
                        "plate_fee": 1234,
                        "contract_fee": 12.34,
                        "permission_user": "ARW",
                        "permission_transaction": "ARW",
                        "permission_invoice": "ARW",
                    },
                }
            }
        },
    }
    return result


def update_user_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def delete_user_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "examples": {
                    "데이터는 유지하고 상태만 'deleted'로 변경된 경우": {
                        "value": {"success": True, "message": "OK", "result": {"withdrawn_object_id": 1}}
                    },
                    "데이터가 삭제된 경우": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {"deleted_object_id": 1},
                        }
                    },
                }
            },
        },
    }
    return result


def login_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 401, 403, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHA"
                    + "iOjE2NTIzMjc0MjgsImlhdCI6MTY1MjMyNjUyOCwic2NvcGUiOiJhY2Nlc3"
                    + "NfdG9rZW4iLCJzdWIiOiIxMDUifQ.uUeS_vH6uhzcaFDfxOyxKaaxwuzAjqzEGZxL_62tsqQ",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHA"
                    + "iOjE2NTQ5MTg1MjgsImlhdCI6MTY1MjMyNjUyOCwic2NvcGUiOiJyZWZyZX"
                    + "NoX3Rva2VuIiwic3ViIjoiMTA1In0.e0PUoa36RxR6G-r-1lOrYYkdW2T2duXkGKJEaP3VO3g",
                }
            }
        },
    }
    return result


def refresh_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 400, 403, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHA"
                    + "iOjE2NTIzMjc0MjgsImlhdCI6MTY1MjMyNjUyOCwic2NvcGUiOiJhY2Nlc3"
                    + "NfdG9rZW4iLCJzdWIiOiIxMDUifQ.uUeS_vH6uhzcaFDfxOyxKaaxwuzAjqzEGZxL_62tsqQ",
                }
            }
        },
    }
    return result


def verify_email_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200, 201, 401, 403, 422]
    for key in to_delete:
        del result[key]
    result[307] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {"application/json": {"example": {"별도의 return값은 존재하지 않으며 {SERVER_URL}으로 redirection됨"}}},
    }
    result[400] = {
        "description": "이메일 토큰이 유효하지 않을 경우",
        "content": {
            "text/html": {"example": {"<html><script>alert('인증 토큰이 유효하지 않습니다!');location.href='/';</script></html>"}}
        },
    }
    result[409] = {
        "description": "DB에서 오류가 발생한 경우",
        "content": {
            "text/html": {"example": {"<html><script>alert('예상치 못한 오류가 발생했습니다!');location.href='/';</script></html>"}}
        },
    }
    return result


def send_password_reset_mail_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 401, 403, 422]
    for key in to_delete:
        del result[key]
    return result


def reset_password_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 401, 403]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def create_insurance_company_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_specific_insurance_company_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"id": 1, "name": "삼성화재"},
                }
            }
        },
    }
    return result


def get_all_insurance_company_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": [{"id": 1, "name": "삼성화재"}, {"id": 2, "name": "제휴사"}],
                }
            }
        },
    }
    return result


def update_insurance_company_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def delete_insurance_company_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"deleted_object_id": 1},
                }
            }
        },
    }
    return result


def create_transaction_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_transaction_table_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "total_length": 3,
                        "transaction_list": [
                            {
                                "id": 3,
                                "date": "2022-02-22",
                                "created_at": "2022-06-04T20:09:49",
                                "insurance_company": "제휴사",
                                "vehicle_id": "222이 2222",
                                "vehicle_model": "홍진호카",
                                "user_name": "김대표",
                                "price": 22,
                                "memo": "",
                                "canceled": True,
                                "cancel_fee": 123456,
                            },
                            {
                                "id": 2,
                                "date": "2022-06-04",
                                "created_at": "2022-06-04T20:08:47",
                                "insurance_company": "제휴사",
                                "vehicle_id": "234나 5678",
                                "vehicle_model": "롤스로이스",
                                "user_name": "김대표",
                                "price": 99999,
                                "memo": "",
                                "canceled": False,
                                "cancel_fee": 0,
                            },
                            {
                                "id": 1,
                                "date": "2022-06-04",
                                "created_at": "2022-06-04T20:08:16",
                                "insurance_company": "애니카",
                                "vehicle_id": "123가 1234",
                                "vehicle_model": "벤츠 S500",
                                "user_name": "김대표",
                                "price": 1234,
                                "memo": "",
                                "canceled": False,
                                "cancel_fee": 0,
                            },
                        ],
                    },
                }
            }
        },
    }
    return result


def get_specific_transaction_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "examples": {
                    "취소 건이 아닌 경우": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {
                                "transaction_id": 1,
                                "transaction_date": "2022-05-12",
                                "created_at": "2022-05-13T13:04:12",
                                "insurance_company_name": "삼성화재",
                                "user_name": "김기사",
                                "price": 1234,
                                "vehicle_id": "123가 1234",
                                "vehicle_model": "모닝",
                                "memo": "",
                                "canceled": False,
                                "cancele_fee": 0,
                            },
                        }
                    },
                    "취소 건인 경우": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {
                                "transaction_id": 1,
                                "transaction_date": "2022-05-12",
                                "created_at": "2022-05-13T13:04:12",
                                "insurance_company_name": "삼성화재",
                                "user_name": "김기사",
                                "price": 1234,
                                "vehicle_id": "123가 1234",
                                "vehicle_model": "모닝",
                                "memo": "",
                                "canceled": True,
                                "cancele_fee": 5000,
                            },
                        }
                    },
                }
            }
        },
    }
    return result


def update_transaction_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def delete_transaction_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    return result


def create_user_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_user_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "user_invoice_extra": [
                            {
                                "id": 1,
                                "name": "명절 보너스",
                                "price": 200000,
                            },
                            {
                                "id": 2,
                                "name": "기타 보너스",
                                "price": 100000,
                            },
                        ],
                    },
                }
            }
        },
    }
    return result


def update_user_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def delete_user_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"deleted_object_id": 1},
                }
            }
        },
    }
    return result


def create_user_invoice_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_user_invoice_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "examples": {
                    "기본 급여": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {
                                "user_id": 2,
                                "contract_fee": 15.0,
                                "plate_fee": 220000,
                                "year": "2022",
                                "month": "02",
                                "transaction_count": 100,
                                "canceled_transaction_count": 5,
                                "revenue": 1000000,
                                "cancel_fee": 25000,
                                "total_revenue": 1025000,
                                "total_contract_fee": 153750,
                                "first_vat": 87125,
                                "first_income": 738375,
                                "extra": [],
                                "second_vat": 0,
                                "second_income": 0,
                                "income": 738375,
                            },
                        }
                    },
                    "기본 급여 외에 증액 또는 감액이 존재하는 경우": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {
                                "user_id": 2,
                                "contract_fee": 15.0,
                                "plate_fee": 220000,
                                "year": "2022",
                                "month": "02",
                                "transaction_count": 100,
                                "canceled_transaction_count": 5,
                                "revenue": 1000000,
                                "cancel_fee": 25000,
                                "total_revenue": 1025000,
                                "total_contract_fee": 153750,
                                "first_vat": 87125,
                                "first_income": 738375,
                                "extra": [
                                    {"name": "명절 보너스", "price": 200000},
                                    {"name": "기타 보너스", "price": 100000},
                                ],
                                "extra_price": 300000,
                                "second_vat": 103837,
                                "second_income": 1142212,
                                "income": 1142212,
                            },
                        }
                    },
                }
            },
        },
    }
    return result


def create_company_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_company_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "user_invoice_extra": [
                            {
                                "id": 1,
                                "name": "기타 수입",
                                "price": 200000,
                            },
                            {
                                "id": 2,
                                "name": "기타 지출",
                                "price": -100000,
                            },
                        ],
                    },
                }
            }
        },
    }
    return result


def update_company_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"updated_object_id": 1},
                }
            }
        },
    }
    return result


def delete_company_invoice_extra_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"deleted_object_id": 1},
                }
            }
        },
    }
    return result


def create_company_invoice_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [200]
    for key in to_delete:
        del result[key]
    return result


def get_company_invoice_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "examples": {
                    "증액 또는 감액이 존재하지 않는 경우": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {
                                "year": "2022",
                                "month": "02",
                                "transaction_count": 100,
                                "canceled_transaction_count": 5,
                                "revenue": 1000000,
                                "cancel_fee": 25000,
                                "total_revenue": 1025000,
                                "total_contract_fee": 153750,
                                "first_vat": 87125,
                                "first_income": 738375,
                                "extra": [],
                                "second_vat": 0,
                                "second_income": 0,
                                "income": 738375,
                            },
                        }
                    },
                    "증액 또는 감액이 존재하는 경우": {
                        "value": {
                            "success": True,
                            "message": "OK",
                            "result": {
                                "user_id": 2,
                                "contract_fee": 15.0,
                                "plate_fee": 220000,
                                "year": "2022",
                                "month": "02",
                                "transaction_count": 100,
                                "canceled_transaction_count": 5,
                                "revenue": 1000000,
                                "cancel_fee": 25000,
                                "total_revenue": 1025000,
                                "total_contract_fee": 153750,
                                "first_vat": 87125,
                                "first_income": 738375,
                                "extra": [
                                    {"name": "명절 보너스", "price": 200000},
                                    {"name": "기타 보너스", "price": 100000},
                                ],
                                "extra_price": 300000,
                                "second_vat": 103837,
                                "second_income": 1142212,
                                "income": 1142212,
                            },
                        }
                    },
                }
            },
        },
    }
    return result


def get_monthly_cancel_fee_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"cancel_fee": 12345},
                }
            }
        },
    }
    return result


def get_monthly_plate_fee_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"plate_fee": 12345},
                }
            }
        },
    }
    return result


def get_monthly_employee_salary_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {"employee_salary": 12345},
                }
            }
        },
    }
    return result


def get_current_revenue_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "revenue": 300000,
                        "rate": 20,
                    },
                }
            }
        },
    }
    return result


def get_current_transaction_count_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "transaction_count": 120,
                        "difference_count": 20,
                    },
                }
            }
        },
    }
    return result


def get_monthly_revenue_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "revenue_list": [
                            {
                                "year": 2022,
                                "month": 4,
                                "revenue": 10000,
                            },
                            {
                                "year": 2022,
                                "month": 5,
                                "revenue": 15000,
                            },
                            {
                                "year": 2022,
                                "month": 6,
                                "revenue": 12000,
                            },
                        ]
                    },
                }
            }
        },
    }
    result[400] = {
        "description": "range 매개변수가 적절하지 않은 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "message": "존재하지 않는 데이터입니다!",
                }
            }
        },
    }
    return result


def get_monthly_member_revenue_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "user_list": [
                            {
                                "user_name": "김기사",
                                "revenue": 15000,
                            },
                            {
                                "user_name": "박기사",
                                "revenue": 12000,
                            },
                            {
                                "user_name": "최기사",
                                "revenue": 10000,
                            },
                        ]
                    },
                }
            }
        },
    }


def get_current_month_member_revenue_rate_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "user_list": [
                            {"user_name": "김기사", "percentage": 40, "difference_persentage": 20},
                            {"user_name": "박기사", "percentage": 30, "difference_persentage": 30},
                            {"user_name": "최기사", "percentage": 30, "difference_persentage": 15},
                        ]
                    },
                }
            }
        },
    }


def get_current_month_insurance_company_rate_response():
    result = deepcopy(DEFAULT_RESPONSES)
    to_delete = [201, 409, 422]
    for key in to_delete:
        del result[key]
    result[200] = {
        "description": "요청이 성공적으로 처리되었을 경우",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "OK",
                    "result": {
                        "company_list": [
                            {"company_name": "애니카", "percentage": 40, "difference_persentage": 20},
                            {"company_name": "삼성화재", "percentage": 30, "difference_persentage": 30},
                            {"company_name": "준영카", "percentage": 30, "difference_persentage": 15},
                        ]
                    },
                }
            }
        },
    }
