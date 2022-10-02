<script>
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Dialog, { Title, Content, Actions, Header } from "@smui/dialog";
  import Textfield from "@smui/textfield";

  import { faPlusCircle } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "fontawesome-svelte";
  import Button, { Label } from "@smui/button";

  import List, {
    Item,
    Graphic,
    Meta,
    Text,
    PrimaryText,
    SecondaryText,
  } from "@smui/list";

  import { UserExtraHandler, user_extra_store } from "~/data/Invoice/UserExtra";

  export let open;
  export let year;
  export let month;
  export let user_id;

  let user_extra_list = [];

  let selection_info = {};
  $: selection_info = user_extra_list.filter(
    (user_extra) => user_extra.id == selection_id
  )[0];

  $: UserExtraHandler._update(user_id, year, month);

  user_extra_store.subscribe((value) => {
    if (value.result) user_extra_list = value.result;
  });

  let new_name = "";
  let new_price = 0;
  $: {
    if (user_id != undefined && year != undefined && month != undefined) {
      UserExtraHandler._update(user_id, year, month);
    }
  }

  let selection_id = 0;
  let selectionIndex;

  $: if (open == true) {
    // update name when moal open
    new_name = "";
  }

  const createUserExtra = (extra_name, price) => {
    UserExtraHandler.create(user_id, year, month, extra_name, price).then(
      ({ status, data }) => {
        if (status == 201) {
          // 요청이 성공적으로 처리되었을 경우
          alert("추가 성공!");
        } else if (status == 401) {
          // 	Token이 유효하지 않은 경우
        } else if (status == 403) {
          // 	Token이 없거나 권한이 부족한 경우
        } else if (status == 409) {
          // DB, 메일 전송 오류 등 예상치 못한 오류가 발생한 경우
        } else if (status == 422) {
          // 	요청 파라미터가 유효하지 않은 경우
        }
      }
    );
  };

  const deleteUserExtra = (extra_id) => {
    UserExtraHandler.delete(user_id, year, month, extra_id).then(
      ({ status, data }) => {
        if (status == 200) {
          // 요청이 성공적으로 처리되었을 경우
          alert("삭제 성공!");
        }
        if (status == 400) {
          // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
          // 1. 이미 정산이 완료되어 수정 또는 삭제가 불가능합니다!
          alert(data.message);
        }
      }
    );
  };

  const updateUserExtra = (extra_id, extra_name, extra_price) => {
    let extra_info = { id: extra_id, name: extra_name, price: extra_price };
    UserExtraHandler.update(user_id, year, month, extra_info).then(
      ({ status, data }) => {
        if (status == 200) {
          // 요청이 성공적으로 처리되었을 경우
          alert("수정 성공!");
        }
        if (status == 400) {
          // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
          // 1. 이미 정산이 완료되어 수정 또는 삭제가 불가능합니다!
          alert(data.message);
        }
      }
    );
  };
</script>

<Dialog
  bind:open
  fullscreen
  aria-labelledby="fullscreen-title"
  aria-describedby="fullscreen-content"
>
  <Header>
    <Title id="fullscreen-title"
      >{year}년 {month}월 추가급여 현황 ({user_id})</Title
    >
  </Header>
  <Content id="fullscreen-content">
    <LayoutGrid>
      <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
        <div class="extra-list">
          <List
            class="demo-list"
            twoLine
            avatarList
            singleSelection
            bind:selectedIndex={selectionIndex}
          >
            {#each user_extra_list as user_extra}
              <Item
                on:SMUI:action={() => (selection_id = user_extra.id)}
                selected={selection_id === user_extra.id}
              >
                <Graphic
                  style="background-image: url(https://place-hold.it/40x40?text={user_extra.name
                    .split(' ')
                    .map((val) => val.substring(0, 1))
                    .join('')}&fontsize=16);
                        "
                />
                <Text>
                  <PrimaryText>{user_extra.name}</PrimaryText>
                  <SecondaryText>{user_extra.id}</SecondaryText>
                </Text>
                <Meta class="material-icons">info</Meta>
              </Item>
            {/each}
            <Item
              on:SMUI:action={() => (selection_id = 0)}
              selected={selection_id === 0}
            >
              <Graphic
                ><FontAwesomeIcon
                  style="width:40px; height:40px; color:#aaaaaa;"
                  icon={faPlusCircle}
                /></Graphic
              >

              <Text>
                <PrimaryText>추가하기</PrimaryText>
                <SecondaryText />
              </Text>
            </Item>
          </List>
        </div>
      </Cell>
      <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
        <div class="extra-edit">
          {#if selection_info}
            <!-- 기존 정보 변경 -->
            <div class="input-wrap">
              <h3>보너스명</h3>
              <Textfield
                variant="outlined"
                bind:value={selection_info["name"]}
                style="height:36px; width:100%;"
              />

              <h3>금액</h3>
              <Textfield
                variant="outlined"
                bind:value={selection_info["price"]}
                style="height:36px; width:100%;"
              />
            </div>
            <div class="action-wrap">
              <Button
                variant="unelevated"
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                on:click={() => deleteUserExtra(selection_id)}
              >
                <Label>삭제</Label>
              </Button>
              <Button
                variant="unelevated"
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                on:click={() =>
                  updateUserExtra(
                    selection_id,
                    selection_info["name"],
                    selection_info["price"]
                  )}
              >
                <Label>적용</Label>
              </Button>
            </div>
          {:else if selection_id == 0}
            <!-- 새로 추가  -->
            <div class="input-wrap">
              <h3>보너스명</h3>
              <Textfield
                variant="outlined"
                bind:value={new_name}
                style="height:36px; width:100%;"
              />
              <h3>금액</h3>
              <Textfield
                variant="outlined"
                bind:value={new_price}
                style="height:36px; width:100%;"
              />
            </div>
            <div class="action-wrap">
              <Button
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                variant="unelevated"
                on:click={() => createUserExtra(new_name, new_price)}
              >
                <Label>추가</Label>
              </Button>
            </div>
          {/if}
        </div>
      </Cell>
    </LayoutGrid>
  </Content>
  <Actions>
    <Button>
      <Label>확인</Label>
    </Button>
  </Actions>
</Dialog>

<style lang="scss">
  .extra-list {
    height: 250px;
    border: 1px solid #9e9e9e;
    border-radius: 10px;
    padding: 10px 0px;
    overflow-y: scroll;
  }

  .extra-edit {
    height: 250px;
    border: 1px solid #9e9e9e;
    border-radius: 10px;
    padding: 10px 50px;
    .input-wrap {
      margin-bottom: 30px;
    }
  }

  .action-wrap {
    display: flex;
    justify-content: flex-end;
    padding: 30px 0px;
  }
</style>
