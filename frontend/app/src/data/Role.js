import { writable, get } from "svelte/store";
import { request } from "~/utils/request";
import { EmployeeHandler } from "~/data/Employee";

export const role_store = writable([]);

export class RoleHandler {
  static init() {
    if (!get(role_store).length) {
      console.log("get", get(role_store));
      RoleHandler._update();
    }
  }

  static _update() {
    return new Promise((resolve, reject) => {
      request("/api/user/role", "get", {}, {}, "access").then(
        ({ status, data }) => {
          if (status == 200) {
            role_store.set(data);
            resolve();
          }
        }
      );
    });
  }

  static create(role_name) {
    return new Promise((resolve, reject) => {
      request(
        "/api/user/role",
        "post",
        {},
        JSON.stringify({ name: role_name }),
        "access"
      ).then(({ status, data }) => {
        if (status == 201) {
          this._update().then(() => {
            EmployeeHandler._update().then(() => {
              resolve({ status, data });
            });
          });
        } else resolve({ status, data });
      });
    });
  }

  static put(id, name) {
    return new Promise((resolve, reject) => {
      request(
        `/api/user/role/${id}`,
        "put",
        {},
        JSON.stringify({ name: name }),
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          this._update().then(() => {
            EmployeeHandler._update().then(() => {
              resolve({ status, data });
            });
          });
        } else resolve({ status, data });
      });
    });
  }

  static delete(id) {
    return new Promise((resolve, reject) => {
      request(`/api/user/role/${id}`, "delete", {}, {}, "access").then(
        ({ status, data }) => {
          if (status == 200) {
            this._update().then(() => {
              EmployeeHandler._update().then(() => {
                resolve({ status, data });
              });
            });
          }
        }
      );
    });
  }
}
