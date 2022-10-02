<script>
  import { createEventDispatcher } from "svelte";

  import DataTable, {
    Head,
    Body,
    Row,
    Cell,
    Pagination,
  } from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Dialog, { Title, Content, Actions } from "@smui/dialog";
  import Button, { Label } from "@smui/button";
  import Tooltip, { Wrapper } from "@smui/tooltip";
  import CircularProgress from "@smui/circular-progress";

  import { faStickyNote } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "fontawesome-svelte";

  import { TransactionHandler, transaction_store } from "~/data/Transaction";
  import TransactionOption from "~/components/Transaction/TransactionOption.svelte";
  const dispatch = createEventDispatcher();

  let delete_modal_open = false;
  let transaction_list = [];

  const requestOpenCreateModal = (target_transaction_id) => {
    dispatch("requestOpenCreateModal", {
      target_transaction_id,
    });
  };

  let delete_id;
  const openDeleteModal = (id) => {
    delete_modal_open = true;
    delete_id = id;
  };

  const deleteTransaction = (id) => {
    TransactionHandler.delete(id).then((status, data) => {
      if (status == 200) {
        alert("삭제가 완료되었습니다!");
      }
    });
  };

  let rowsPerPage = 10;
  let currentPage = 0;
  let start = 0;
  let end = 10;
  let total_length = 0;
  let lastPage = 0;

  /* input tag 선택지 List */

  let lookup_option = {
    start_date: "",
    end_date: "",
    user_id: "",
    insurance_company_id: -1,
    page: currentPage,
    limit: rowsPerPage,
    canceled_type: "ALL",
    order_by: "transaction_id",
    order_type: "desc",
  };

  transaction_store.subscribe((value) => {
    if (value.result) {
      total_length = value.result.total_length;
      transaction_list = value.result.transaction_list;
    }
  });

  $: {
    start = currentPage * rowsPerPage;
    end = Math.min(start + rowsPerPage, total_length);
    lastPage = Math.max(Math.ceil(total_length / rowsPerPage) - 1, 0);

    lookup_option["page"] = currentPage;
    TransactionHandler._update(lookup_option);
  }
</script>

<TransactionOption bind:option={lookup_option} />

{#if transaction_list.length > 0}
  <DataTable table$aria-label="People list" style="width: 100%;">
    <Head>
      <Row>
        <Cell>업무유형</Cell>
        <Cell>업무날짜</Cell>
        <Cell>차량번호</Cell>
        <Cell>차종</Cell>
        <Cell>담당자</Cell>
        <Cell>금액</Cell>
        <Cell>등록날짜</Cell>
        <Cell>비고</Cell>
        <Cell style="text-align:center;">조치</Cell>
      </Row>
    </Head>
    <Body>
      {#each transaction_list as transaction}
        <Row class={transaction.canceled ? "canceled" : ""}>
          <Cell>{transaction.insurance_company_name}</Cell>
          <Cell>{transaction.date}</Cell>
          <Cell>{transaction.vehicle_id}</Cell>
          <Cell>{transaction.vehicle_model}</Cell>
          <Cell>{transaction.user_name}</Cell>
          <Cell>{transaction.price}</Cell>
          <Cell>{transaction.created_at}</Cell>
          <Cell>
            {#if transaction.memo != ""}
              <Wrapper>
                <FontAwesomeIcon icon={faStickyNote} style="color:yellow;" />
                <Tooltip xPos="start">{transaction.memo}</Tooltip>
              </Wrapper>
            {/if}
          </Cell>
          <Cell style="text-align:center;">
            <IconButton
              class="material-icons"
              on:click={() => {
                requestOpenCreateModal(transaction);
              }}>edit</IconButton
            >
            <IconButton
              class="material-icons"
              on:click={() => {
                openDeleteModal(transaction.id);
              }}>delete_outline</IconButton
            >
          </Cell>
        </Row>
      {/each}
    </Body>
    <Pagination slot="paginate">
      <svelte:fragment slot="total">
        {start + 1}-{end} of {total_length}
      </svelte:fragment>

      <IconButton
        class="material-icons"
        action="first-page"
        title="First page"
        on:click={() => (currentPage = 0)}
        disabled={currentPage === 0}>first_page</IconButton
      >
      <IconButton
        class="material-icons"
        action="prev-page"
        title="Prev page"
        on:click={() => currentPage--}
        disabled={currentPage === 0}>chevron_left</IconButton
      >
      <IconButton
        class="material-icons"
        action="next-page"
        title="Next page"
        on:click={() => currentPage++}
        disabled={currentPage === lastPage}>chevron_right</IconButton
      >
      <IconButton
        class="material-icons"
        action="last-page"
        title="Last page"
        on:click={() => (currentPage = lastPage)}
        disabled={currentPage === lastPage}>last_page</IconButton
      >
    </Pagination>
  </DataTable>
{:else}
  <div class="exception">
    <div class="message-wrap">
      <CircularProgress
        class="my-four-colors"
        style="height: 64px; width: 64px;"
        indeterminate
        fourColor
      />
      <span>데이터를 가져오고있습니다.</span>
    </div>
  </div>
{/if}

<Dialog bind:open={delete_modal_open}>
  <Title>삭제</Title>
  <Content>{delete_id}를 삭제하시겠습니까?</Content>
  <Actions>
    <Button>
      <Label>No</Label>
    </Button>
    <Button
      on:click={() => {
        deleteTransaction(delete_id);
      }}
    >
      <Label>Yes</Label>
    </Button>
  </Actions>
</Dialog>

<style lang="scss">
  :global(.canceled) {
    background-color: #ff8282;
  }

  .exception {
    padding: 50px 0px;
    text-align: center;
    .message-wrap {
      display: flex;
      flex-direction: row;
    }
  }
</style>
