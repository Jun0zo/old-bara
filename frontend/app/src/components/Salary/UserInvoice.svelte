<script>
  import Select, { Option } from "@smui/select";
  import Button, { Label } from "@smui/button";
  import { EmployeeHandler, employee_store } from "~/data/Employee";
  import UserExtraModal from "~/components/Salary/UserExtraModal.svelte";

  import { FontAwesomeIcon } from "fontawesome-svelte";
  import { faExclamationTriangle } from "@fortawesome/free-solid-svg-icons";

  import {
    UserInvoiceHandler,
    user_invoice_store,
  } from "~/data/Invoice/UserInvoice";

  import { isToday } from "~/utils/date";

  export let year;
  export let month;

  const openUserExtraModal = () => {
    user_extra_modal_open = true;
    console.log(user_extra_modal_open);
  };

  $: {
    if (
      target_employee_id != undefined &&
      year != undefined &&
      month != undefined
    ) {
      UserInvoiceHandler._update(target_employee_id, year, month);
    }
  }

  let invoice = {};
  let employee_list = [];
  let target_employee_id = undefined;

  let user_extra_modal_open = false;

  EmployeeHandler.init();
  employee_store.subscribe((value) => {
    if (value.result) employee_list = value.result;
  });

  user_invoice_store.subscribe((value) => {
    if (value.result) invoice = value.result;
  });

  const secteion1 = {
    item_names: [
      "transaction_count",
      "revenue",
      "total_contract_fee",
      "total_revenue",
    ],
    item_names_ko: [
      "transaction_count",
      "revenue",
      "total_contract_fee",
      "total_revenue",
    ],
  };

  const secteion2 = {
    item_names: [
      "canceled_transaction_count",
      "cancel_fee",
      "contract_fee",
      "first_vat",
      "first_income",
    ],
    item_names_ko: [
      "canceled_transaction_count",
      "cancel_fee",
      "contract_fee",
      "first_vat",
      "first_income",
    ],
  };

  const secteion3 = {
    item_names: ["extra", "plate_fee", "second_vat", "second_income"],
    item_names_ko: ["extra", "plate_fee", "second_vat", "second_income"],
  };
</script>

<div class="container">
  <div class="action-wrap">
    <Select
      style="width:140px;"
      anchor$style="height:40px;"
      variant="outlined"
      bind:value={target_employee_id}
      label="직원"
    >
      {#each employee_list as employee}
        <Option value={String(employee.id)}>{employee.name}</Option>
      {/each}
    </Select>  

    {#if invoice.hasOwnProperty("user_id") && isToday(year, month)}
      <Button
        variant="unelevated"
        style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
        on:click={() => {
          openUserExtraModal();
        }}
      >
        <Label>추가급여관리</Label>
      </Button>
    {/if}
  </div>

  <div class="invoice-wrap">
    {#if invoice.hasOwnProperty("user_id")}
      <div class="invoice-section">
        {#each secteion1.item_names as item_name, idx}
          <div class="invoice-item">
            <div>{secteion1["item_names_ko"][idx]}</div>
            <div>{invoice[item_name]}</div>
          </div>
        {/each}
      </div>
      <div class="invoice-section">
        {#each secteion2.item_names as item_name, idx}
          <div class="invoice-item">
            <div>{secteion2["item_names_ko"][idx]}</div>
            <div>{invoice[item_name]}</div>
          </div>
        {/each}
      </div>

      <div class="invoice-section">
        {#each secteion3.item_names as item_name, idx}
          {#if item_name == "extra"}
            {#each invoice["extra"] as extra}
              <div class="invoice-item">
                <div>{extra["name"]}</div>
                <div>{extra["price"]}</div>
              </div>
            {/each}
          {:else}
            <div class="invoice-item">
              <div>{secteion3["item_names_ko"][idx]}</div>
              <div>{invoice[item_name]}</div>
            </div>
          {/if}
        {/each}
      </div>
    {:else}
      <div class="error">
        <FontAwesomeIcon
          style="font-size:50px; margin-bottom:10px;"
          icon={faExclamationTriangle}
        />
        <span>직원을 선택해주세요!</span>
      </div>
    {/if}
  </div>

  <UserExtraModal
    bind:open={user_extra_modal_open}
    user_id={target_employee_id}
    {year}
    {month}
  />
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .action-wrap {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .invoice-wrap {
    flex: 1;
    padding: 15px 0px;
  }

  .invoice-section {
    margin-bottom: 40px;
  }

  .invoice-item {
    display: flex;
    justify-content: space-between;
    font-size: 20px;
    border-bottom: 1px solid #e4e4e4;
    padding: 5px;
  }

  .error {
    display: flex;
    flex-direction: column;
    margin: auto;
    text-align: center;
  }
</style>
