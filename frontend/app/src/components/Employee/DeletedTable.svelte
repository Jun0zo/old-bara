<script>
  import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Dialog, { Title, Content, Actions } from "@smui/dialog";
  import Button, { Label } from "@smui/button";
  import { FontAwesomeIcon } from "fontawesome-svelte";
  import { faExclamationTriangle } from "@fortawesome/free-solid-svg-icons";

  import { EmployeeHandler, employee_store } from "~/data/Employee";

  let open = false;
  let target_id;

  let deleted_employee_list = [];
  EmployeeHandler.init();
  employee_store.subscribe((value) => {
    if (value.result)
      deleted_employee_list = value.result.filter(
        (employee) => employee.status == "deleted"
      );
  });

  function openModal(id) {
    open = true;
    target_id = id;
  }

  const putEmployee = (target_id) => {};  
</script>

<DataTable table$aria-label="People list" style="width: 100%;">
  <Head>
    <Row>
      <Cell columnId="email">이메일</Cell>
      <Cell columnId="name">이름</Cell>
      <Cell style="text-align:center;">조치</Cell>
    </Row>
  </Head>
  <Body>
    {#if deleted_employee_list.length > 0}
      {#each deleted_employee_list as deleted_employee}
        <Row>
          <Cell>{deleted_employee.email}</Cell>
          <Cell>{deleted_employee.name}</Cell>
          <Cell style="text-align:center;">
            <IconButton
              class="material-icons"
              on:click={() => {
                openModal(deleted_employee.id);
              }}>check</IconButton
            >
          </Cell>
        </Row>
      {/each}
    {:else}
      <div class="warn">
        <FontAwesomeIcon
          style="font-size:50px; margin-bottom:10px;"
          icon={faExclamationTriangle}
        />
        <span>표시할 직원이 없습니다.</span>
      </div>
    {/if}
  </Body>
</DataTable>

<Dialog
  bind:open
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Title id="simple-title">복구</Title>
  <Content id="simple-content">{target_id}를 복구하시겠습니까?</Content>
  <Actions>
    <Button on:click={() => putEmployee(target_id)}>
      <Label>OK</Label>
    </Button>
  </Actions>
</Dialog>

<style>
  .warn {
    display: flex;
    flex-direction: column;
    text-align: center;
    position:relative;
    left:50%;
    transform: translateX(-50%);
  }
</style>
