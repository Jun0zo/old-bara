import { writable, get } from "svelte/store";
import { request } from "~/utils/request";
import { dateFormatting } from "~/utils/date";

export const company_invoice_store = writable({});

export class CompanyInvoiceHandler {
  static init(user_id, year, month) {
    if (!Object.keys(get(company_invoice_store)).length) {
      console.log("get", get(company_invoice_store));
      CompanyInvoiceHandler._update(user_id, year, month);
    }
  }

  static _update(year, month) {
    month = dateFormatting(month);
    return new Promise((resolve, reject) => {
      request(
        `/api/invoice/company?year=${year}&month=${month}`,
        "get",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          company_invoice_store.set(data);
          resolve();
        }
      });
    });
  }

  static create(year, month) {
    return new Promise((resolve, reject) => {
      request(
        "/api/invoice/company",
        "post",
        {},
        JSON.stringify({ year, month }),
        "access"
      ).then(({ status, data }) => {
        if (status == 201) {
          resolve({ status, data });
        }
      });
    });
  }
}
