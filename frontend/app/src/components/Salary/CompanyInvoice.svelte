<script>
  import Button, { Label } from "@smui/button";
  import CompanyExtraModal from "~/components/Salary/CompanyExtraModal.svelte";
  import { FontAwesomeIcon } from "fontawesome-svelte";
  import { faExclamationTriangle } from "@fortawesome/free-solid-svg-icons";

  import {
    CompanyInvoiceHandler,
    company_invoice_store,
  } from "~/data/Invoice/CompanyInvoice";
  import { isToday } from "~/utils/date";

  export let year;
  export let month;

  const openCompanyExtraModal = () => {
    company_extra_modal_open = true;
  };

  $: {
    if (year != undefined && month != undefined)
      CompanyInvoiceHandler._update(year, month);
  }

  let invoice = {};

  let company_extra_modal_open = false;

  company_invoice_store.subscribe((value) => {
    if (value.result) invoice = value.result;
  });

  const secteion = {
    item_names: [
      "plate_fee",
      "rental_fee",
      "income",
      "revenue",
      "employee_salary",
      "maintenance_fee",
      "extra",
    ],
    item_names_ko: [
      "plate_fee",
      "rental_fee",
      "income",
      "revenue",
      "employee_salary",
      "maintenance_fee",
      "extra",
    ],
  };

</script>

<div class="container">
  <div class="action-wrap">
    {#if invoice.hasOwnProperty("id") && isToday(year, month)}
      <Button
        variant="unelevated"
        style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
        on:click={() => {
          openCompanyExtraModal();
        }}
      >
        <Label>추가급여관리</Label>
      </Button>
    {/if}
  </div>

  <div class="invoice-wrap">
    {#if invoice.hasOwnProperty("id") && !isToday(year, month)}
      {#each secteion.item_names as item_name, idx}
        {#if item_name == "extra"}
          {#each invoice["extra"] as extra}
            <div>{extra["name"]}</div>
            <div>{extra["price"]}</div>
          {/each}
        {:else}
          <div class="invoice-item">
            <div>{secteion["item_names_ko"][idx]}</div>
            <div>{invoice[item_name]}</div>
          </div>
        {/if}
      {/each}
    {:else}
      <div class="error">
        <FontAwesomeIcon
          style="font-size:50px; margin-bottom:10px;"
          icon={faExclamationTriangle}
        />
        <span>모든 직원의 금월 급여가 정산된 이후에 조회 가능합니다!</span>
      </div>
    {/if}
  </div>
</div>

<CompanyExtraModal bind:open={company_extra_modal_open} {year} {month} />

<style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .action-wrap {
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }

  .invoice-wrap {
    flex: 1;
    padding: 15px 0px;
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
