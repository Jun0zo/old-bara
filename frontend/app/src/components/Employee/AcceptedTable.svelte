<script>
  import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Dialog, { Title, Content, Actions } from "@smui/dialog";
  import Button, { Label } from "@smui/button";
  import { EmployeeHandler, employee_store } from "~/data/Employee";

  let open = false;
  let delete_id;

  let employee_list = [];
  EmployeeHandler.init();
  employee_store.subscribe((value) => {
    if (value.result) employee_list = value.result;
    console.log("emp", employee_list);
  });

  function openModal(id) {
    open = true;
    delete_id = id;
  }

  const delete_employee = (user_id) => {
    EmployeeHandler.delete(user_id).then(({ status, data }) => {
      if (status == 200) {
        alert("정상적으로 삭제되었습니다!");
      } else if (status == 400) {
        //  요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
        // 1. 본인계정 삭제
        alert(data.messaage);
      } else if (status == 401) {
        //  Token이 유효하지 않은 경우
      } else if (status == 403) {
        //  Token이 없거나 권한이 부족한 경우
      } else if (status == 422) {
        //  요청 파라미터가 유효하지 않은 경우
      }
    });
  };
</script>

<DataTable table$aria-label="People list" style="width: 100%;">
  <Head>
    <Row>
      <Cell columnId="email">이메일</Cell>
      <Cell columnId="role_name">직급</Cell>
      <Cell columnId="name">이름</Cell>
      <Cell style="text-align:center;">탈퇴</Cell>
    </Row>
  </Head>
  <Body>
    {#each employee_list as employee}
      {#if employee.status == "accepted"}
        <Row>
          <Cell>{employee.email}</Cell>
          <Cell>{employee.role_name}</Cell>
          <Cell>{employee.name}</Cell>
          <Cell style="text-align:center;"
            ><IconButton
              class="material-icons"
              on:click={() => {
                openModal(employee.id);
              }}>delete_outline</IconButton
            ></Cell
          >
        </Row>
      {/if}
    {/each}
  </Body>
</DataTable>

<Dialog
  bind:open
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Title id="simple-title">삭제</Title>
  <Content id="simple-content">{delete_id}를 삭제하시겠습니까?</Content>
  <Actions>
    <Button>
      <Label>No</Label>
    </Button>
    <Button on:click={() => delete_employee(delete_id)}>
      <Label>Yes</Label>
    </Button>
  </Actions>
</Dialog>
