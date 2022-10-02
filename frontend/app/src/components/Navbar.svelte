<script>
  import { beforeUpdate } from "svelte";
  import { fly } from "svelte/transition";

  import IconButton from "@smui/icon-button";
  import Button, { Group, Label } from "@smui/button";
  import { Input } from "@smui/textfield";
  import Paper from "@smui/paper";
  import { Icon } from "@smui/common";

  import { FontAwesomeIcon } from "fontawesome-svelte";
  import { faUser, faSignOut } from "@fortawesome/free-solid-svg-icons";

  import { sidebar_enabled_ } from "~/store";
  import { get_userId_from_jwt, get_userInfo_from_id } from "~/utils/account";
  import { request } from "~/utils/request";

  let dropdown_show = false;
  let user_name = "";
  let user_role = "";
  let is_compact = false;
  let value = "";

  let is_login = false;

  document.onload = () => {
    document
      .querySelector(":not(.dr  opdown-menu.show)")
      .addEventListener("click", (event) => {
        let target = event.target;
        if (
          target.classList.contains("user-info-wrap") ||
          target.parentNode.classList.contains("user-info-wrap") ||
          target.parentNode.parentNode.classList.contains("user-info-wrap")
        ) {
        } else {
          dropdown_show = false;
        }
      });
  };

  const refresh_token = () => {
    request("/api/user/token/refresh", "get", {}, {}, "refresh").then(
      ({ status, data }) => {
        if (status == 200) {
          localStorage.setItem("access_token", data.access_token);
          let user_id = get_userId_from_jwt(data.access_token);
          get_userInfo_from_id(user_id)
            .then((user_info) => {
              console.log("user info :", user_info);
              user_name = user_info.name;
              user_role = user_info.role_name;
              is_login = true;
            })
            .catch((e) => {
              console.log("er", e);
            });
        } else if (status == 401) {
          // Token이 유효하지 않은 경우
          localStorage.clear();
          sessionStorage.clear();
          is_login = false;
          alert("세션이 만료되었습니다. 다시 로그인해 주세요");
          window.location.href = "/login";
        } else {
          alert("?", status);
        }
      }
    );
  };

  const toggleMenu = () => {
    sidebar_enabled_.update((value) => !value);
  };

  const logout = () => {
    localStorage.clear();
    sessionStorage.clear();
    is_login = false;
    alert("로그아웃 되었습니다.");
    window.location.href = "/login";
  };

  const controlModal = (status) => {
    // status = true of false
    if (dropdown_show) {
      status = false;
    }
    dropdown_show = status;
  };

  beforeUpdate(async () => {
    refresh_token();
  });
</script>

<nav class="navbar" mode={is_compact}>
  <ul class="left-menu">
    <div class="bars-wrap">
      <IconButton class="material-icons" on:click={toggleMenu}>menu</IconButton>
    </div>

    {#if is_login == true}
      <Group class="search-wrap">
        <Paper class="search" variant="unelevated">
          <Icon
            class="material-icons"
            style="margin-right:10px; color:#6c757d;"
          >
            search
          </Icon>
          <Input
            bind:value
            on:keydown={() => {}}
            style="color:var(--bara-body-color);"
            placeholder="Search"
            class="solo-input"
          />
        </Paper>
        <Button
          variant="unelevated"
          style=" background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245
        / 50%); "
        >
          <Label>Search</Label>
        </Button>
      </Group>
    {/if}
  </ul>
  <ul class="right-menu">
    {#if is_login == false}
      <div />
    {:else}
      <li class="user-info">
        <div
          class="user-info-wrap"
          on:click={() => {
            controlModal(true);
          }}
        >
          <div class="image">
            <img src="static/images/dummy_profile.png" alt="" />
          </div>
          <div class="title">
            <span class="name">{user_name}</span>
            <span class="role">{user_role}</span>
          </div>
        </div>
        {#if dropdown_show == true}
          <div class="dropdown-menu" transition:fly={{ y: 10, duration: 500 }}>
            <div class="dropdown-header">환영합니다</div>
            <a class="dropdown-list" href="javascript(0);">
              <div class="item-wrap">
                <FontAwesomeIcon icon={faUser} style="margin-right:5px" />
                <span>내 정보</span>
              </div>
            </a>
            <a class="dropdown-list" href="#" on:click={logout}>
              <div class="item-wrap">
                <FontAwesomeIcon icon={faSignOut} style="margin-right:5px" />
                <span>로그아웃</span>
              </div>
            </a>
          </div>
        {:else}
          <div />
        {/if}
      </li>
    {/if}
  </ul>
</nav>

<style lang="scss">
  .navbar {
    position: fixed;
    top: 0;
    right: 0;
    width: 100%;
    min-height: 70px;
    background-color: var(--bara-navbar-background-color);
    display: flex;
    justify-content: space-between;
    padding: 0px 30px;
    box-shadow: var(--bara-navbar-shadow);
    z-index: 1;
    width: calc(100% - var(--bara-side-navbar-width) - 60px);
    :global(.menu-icon) {
      display: none;
    }
    .left-menu {
      display: flex;
      align-items: center;
      color: var(--bara-navbar-light-brand-color);
      :global(.search) {
        display: flex;
        align-items: center;
        height: 36px;
        padding: 0px 10px;
        background-color: #f1f3fa;
      }
      .bars-wrap {
        display: flex;
        align-items: center;
        margin-right: 15px;
      }
    }

    .right-menu {
      display: flex;
      align-items: center;

      & li:hover {
        cursor: pointer;
      }
      img {
        width: 2rem;
        border-radius: 5rem;
      }

      .user-info {
        & {
          background-color: gray;
          height: 100%;
        }
        .user-info-wrap {
          border-left: 1px solid #f1f3f9;
          display: flex;
          align-items: center;
          height: 100%;
          background-color: #fafbfd;
          padding: 0px 20px;
          .title {
            display: flex;
            flex-direction: column;
            margin-left: 10px;
            .name {
              color: #99a7ad;
              font-size: 16px;
              line-height: 18px;
            }
            .role {
              color: #99a7ad;
              font-size: 14px;
              line-height: 18px;
            }
          }
        }

        .dropdown-menu {
          & {
            position: absolute;
            top: 100%;
            background-color: white;
            min-width: 124px;
            border: 1px solid var(--bara-dropdown-border-color);
            border-radius: 3px;
          }

          .dropdown-header {
            padding: 10px;
            text-align: center;
          }
          .dropdown-header:hover {
            cursor: default;
          }
          .dropdown-list {
            display: flex;
            justify-content: center;
            padding: 8px 0px;
            color: #6c757d;
            font-size: 14.5px;
            .item-wrap {
              width: 70%;
            }
          }
          .dropdown-list:hover {
            background-color: var(--bara-dropdown-link-hover-background-color);
            color: black;
          }
        }
      }
    }
  }

  :global(.container[sidebar-enabled="false"] .navbar) {
    & {
      width: calc(100% - var(--bara-side-navbar-small-width) - 60px);
    }

    // .user-info .title,
    // :global(.search-wrap) {
    //   display: none;
    // }
  }

  @media (max-width: 975px) {
    .navbar {
      width: calc(100% - var(--bara-side-navbar-small-width) - 60px);
      .user-info .title,
      :global(.search-wrap) {
        display: none;
      }
    }

    :global(.container[sidebar-enabled="false"] .navbar) {
      & {
        width: calc(100% - 60px);
      }
    }
  }

  @media (max-width: 576px) {
    .navbar {
      & {
        width: calc(100% - 60px);
      }
      :global(.menu-icon) {
        display: block;
      }
    }
  }
</style>
