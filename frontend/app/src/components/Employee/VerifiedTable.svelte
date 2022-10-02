<script>
  import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Dialog, { Title, Content, Actions, Header } from "@smui/dialog";
  import Button, { Label } from "@smui/button";
  import { FontAwesomeIcon } from "fontawesome-svelte";
  import { faExclamationTriangle } from "@fortawesome/free-solid-svg-icons";

  import SettingModal from "~/components/Employee/SettingModal.svelte";
  import { EmployeeHandler, employee_store } from "~/data/Employee";

  let verity_modal_open = false;
  let setting_modal_open = false;

  let verified_users = [];
  let target_info = { id: 0, name: "" };
  let action = "";

  let employee_list = [];
  employee_store.subscribe((value) => {
    if (value.result) employee_list = value.result;
  });

  const open_verify_modal = (id, name, _action) => {
    verity_modal_open = true;
    action = _action;
    target_info = { id, name };
    console.log("test :", target_info);
  };

  const open_setting_modal = () => {
    setting_modal_open = true;
  };

  const reject_employee = (target_id) => {
    EmployeeHandler.reject(target_id).then(({ status, data }) => {
      if (status == 200) {
        alert("정상적으로 삭제되었습니다!");
      } else if (status == 400) {
        //  요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
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
      <Cell columnId="name">이름</Cell>
      <Cell style="text-align:center;">조치</Cell>
    </Row>
  </Head>
  <Body>
    {#if verified_users.length > 0}
      {#each verified_users as veverified_user}
        <Row>
          <Cell>{veverified_user.email}</Cell>
          <Cell>{veverified_user.name}</Cell>
          <Cell style="text-align:center;">
            <IconButton
              class="material-icons"
              style="color:green;"
              on:click={() => {
                open_verify_modal(
                  veverified_user.id,
                  veverified_user.name,
                  "accept"
                );
              }}>check</IconButton
            >
            <IconButton
              class="material-icons"
              style="color:red;"
              on:click={() => {
                open_verify_modal(
                  veverified_user.id,
                  veverified_user.name,
                  "reject"
                );
              }}>X</IconButton
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
  bind:open={verity_modal_open}
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
  {#if action == "reject"}
    <Title>거부</Title>
    <Content>{target_info["id"]}를 거부하시겠습니까?</Content>
  {/if}
  {#if action == "accept"}
    <Title id="simple-title">승인</Title>
    <Content id="simple-content"
      >{target_info["id"]}를 승인하시겠습니까?</Content
    >
  {/if}
  <Actions>
    <Button>
      <Label>No</Label>
    </Button>
    {#if action == "reject"}
      <Button
        on:click={() => {
          reject_employee(target_info["id"]);
        }}
      >
        <Label>Yes</Label>
      </Button>
    {:else}
      <Button
        on:click={() => {
          open_setting_modal(target_info["id"]);
        }}
      >
        <Label>Yes</Label>
      </Button>
    {/if}
  </Actions>
</Dialog>

<SettingModal bind:open={setting_modal_open} {target_info} />

<style>
  .warn {
    display: flex;
    flex-direction: column;
    text-align: center;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
  }
</style>
