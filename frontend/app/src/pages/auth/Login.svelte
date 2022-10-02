<script>
  import AuthTemplate from "../../templates/AuthTemplate.svelte";
  import { navigate } from "svelte-routing";
  import Button, { Label } from "@smui/button";
  import { Input } from "@smui/textfield";
  import Paper from "@smui/paper";

  import { fade, scale } from "svelte/transition";

  import BaraCard, { Body } from "~/components/bara-card";
  import { request } from "~/utils/request";

  let email = "";
  let password = "";

  const login = (e) => {
    if (email == "" || password == "") {
      alert("이메일이나 비밀번호는 빈 값이 올 수 없습니다!");
      return;
    }
    request(
      "/api/user/login",
      "post",
      { accept: "application/json", "Content-Type": "application/json" },
      JSON.stringify({
        email: email,
        password: password,
      })
    ).then(({ status, data }) => {
      console.log(status);
      console.log(data);
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        alert("로그인 성공!");
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        navigate("/dashboard");
      } else if (status == 400) {
        // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
        // 1. 빈 값일때
        // 2. 비밀번호가 틀렸을 때
        alert(data.message);
      } else if (status == 422) {
        // 요청 파라미터가 유효하지 않은 경우
        if (data.detail[0]["type"] == "value_error.email")
          alert("이메일 형식이 잘못되었습니다");
        else {
          alert("요청이 잘못되었습니다");
        }
      }
    });
  };

  const find_password = () => {
    if (email == "") {
      alert("이메일을 채워넣어주세요");
      return;
    }
  };

  const handle_key_down = (e) => {
    const k = e.target.value;
    if (e.keyCode === 13) {
      login();
    }
  };
</script>

<AuthTemplate>
  <div
    class="card-wrap"
    in:scale={{ duration: 500 }}
    out:fade={{ duration: 500 }}
  >
    <BaraCard
      style="position:relative; 
      padding:0px 20px;
      background-color:#313a46;
      "
    >
      <Body>
        <div id="container">
          <div class="title-wrap">
            <img src="static/images/bara_logo_hrzt.svg" alt="logo" />
          </div>
          <div
            class="input-wrap"
            on:keydown={(e) => {
              handle_key_down(e);
            }}
          >
            <div class="input-component">
              <div class="label">이메일</div>
              <Paper
                class="input-box"
                variant="unelevated"
                style="background-color:#202325; margin-bottom:5px;"
              >
                <Input
                  bind:value={email}
                  style="background-color:#202325; color:#dcddde;"
                  placeholder="Search"
                  class="solo-input"
                />
              </Paper>
            </div>
            <div class="input-component">
              <div class="label">비밀번호</div>
              <Paper
                class="input-box"
                variant="unelevated"
                style="background-color:#202325; margin-bottom:5px;"
              >
                <Input
                  bind:value={password}
                  type="password"
                  style="background-color:#202325; color:#dcddde;"
                  placeholder="Search"
                  class="solo-input"
                />
              </Paper>
              <div class="addon-text-wrap">
                <sapn
                  class="action-content-text"
                  on:click={() => {
                    find_password();
                  }}
                >
                  비밀번호를 잊으셨나요?
                </sapn>
              </div>
            </div>
          </div>

          <div class="action-wrap">
            <Button
              variant="unelevated"
              style="width:100%;background-color:rgb(66 156 215); box-shadow:0 2px 6px 0 rgb(114 124 245
            / 50%); margin-bottom:10px;"
              on:click={() => {
                login();
              }}
            >
              <Label>로그인</Label>
            </Button>
            <div class="addon-text-wrap">
              <span class="content-text">아직 회원이 아니신가요?</span>
              <span
                class="action-content-text"
                on:click={() => {
                  window.location.href = "/register";
                }}>가입하기</span
              >
            </div>
          </div>
        </div>
      </Body>
    </BaraCard>
  </div>
</AuthTemplate>

<style lang="scss">
  .card-wrap {
    margin: auto;
    width: 470px;
  }

  @media (max-width: 576px) {
    .card-wrap {
      width: 90%;
    }
  }

  #container {
    display: flex;
    flex-direction: column;
    :global(.input-box) {
      display: flex;
      align-items: center;
      height: 40px;
      padding: 0px 10px;
    }

    .content-text {
      font-size: 14px;
      color: #6c6f75;
    }

    .action-content-text {
      font-size: 14px;
      color: #02aef4;
    }

    .action-content-text:hover {
      cursor: pointer;
      text-decoration: underline;
    }

    .title-wrap {
      padding: 20px;
      margin-bottom: 20px;
    }

    .input-wrap {
      margin-bottom: 15px;
      .input-component {
        margin-bottom: 10px;
      }
      .label {
        font-size: 12px;
        color: #b9bbbe;
        margin-bottom: 10px;
      }
    }
  }
</style>
