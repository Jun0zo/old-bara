import { writable, get } from "svelte/store";
import { request } from "~/utils/request";

export let insurance_company_store = writable([]);

export class InsuranceCompanyHandler {
  static init() {
    if (!get(insurance_company_store).length) {
      InsuranceCompanyHandler._update();
    }
  }

  static _update() {
    return new Promise((resolve, reject) => {
      request(
        "/api/transaction/insurancecompany",
        "get",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          insurance_company_store.set(data);
          resolve();
        }
      });
    });
  }

  static create(name) {
    return new Promise((resolve, reject) => {
      request(
        "/api/transaction/insurancecompany",
        "post",
        {},
        JSON.stringify({ name }),
        "access"
      ).then(({ status, data }) => {
        if (status == 201) {
          this._update().then(() => resolve({ status, data }));
        } else resolve({ status, data });
      });
    });
  }

  static delete(id) {
    return new Promise((resolve, reject) => {
      request(
        `/api/transaction/insurancecompany/${id}`,
        "delete",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          this._update().then(() => resolve({ status, data }));
        } else resolve({ status, data });
      });
    });
  }

  static update(id, name) {
    return new Promise((resolve, reject) => {
      request(
        `/api/transaction/insurancecompany/${id}`,
        "put",
        {},
        JSON.stringify({ name }),
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          this._update().then(() => resolve({ status, data }));
        } else resolve({ status, data });
      });
    });
  }
}
