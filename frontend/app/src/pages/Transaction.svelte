<script>
  import Button, { Label } from "@smui/button";

  import Template from "~/templates/Template.svelte";
  import TransactionTable from "~/components/Transaction/TransactionTable.svelte";
  import TransactionUpdateModal from "~/components/Transaction/TransactionUpdateModal.svelte";
  import InsuranceCompanyModal from "~/components/Transaction/InsuranceCompanyModal.svelte";
  import BaraCard, { Body, Head } from "~/components/bara-card";

  import { getTodayString } from "~/utils/date";

  let nav_info = { active_name: "transaction", title_name: "Transactions" };
  let transaction_modal_open = false;
  let insurance_company_modal_open = false;
  let target_transaction = {};
  let new_transaction = true;

  const handleTragetTransactionId = (event) => {
    openTransactionUpdateModal(event.detail.target_transaction_id);
  };

  const openTransactionUpdateModal = (transaction) => {
    if (Object.keys(transaction).length == 0) {
      transaction = {
        user_id: 0,
        insurance_company_id: 0,
        vehicle_id: "",
        vehicle_model: "",
        date: getTodayString(),
        price: 0,
        memo: "",
      };
      new_transaction = true;
    } else {
      new_transaction = false;
    }
    console.log("check", new_transaction);
    target_transaction = transaction;
    transaction_modal_open = true;
  };

  const openInsuranceCompanyModal = () => {
    insurance_company_modal_open = true;
  };
</script>

<Template {nav_info}>
  <div class="action-wrap">
    <Button
      variant="unelevated"
      style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); margin-right:15px;"
      on:click={() => openInsuranceCompanyModal()}
    >
      <Label>제휴사추가</Label>
    </Button>
    <Button
      variant="unelevated"
      style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
      on:click={() => openTransactionUpdateModal({})}
    >
      <Label>업무추가</Label>
    </Button>
  </div>
  <BaraCard>
    <Head>
      업무현황
    </Head>
    <Body>
      <TransactionTable on:requestOpenCreateModal={handleTragetTransactionId} />
    </Body>
  </BaraCard>
</Template>

<TransactionUpdateModal
  bind:open={transaction_modal_open}
  {target_transaction}
  {new_transaction}
/>

<InsuranceCompanyModal bind:open={insurance_company_modal_open} />

<style>
  .action-wrap {
    display: flex;
    justify-content: flex-end;
    padding: 30px 0px;
  }
</style>
