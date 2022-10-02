<script>
  import { link } from "svelte-routing";
  import {
    faPieChart,
    faUserGroup,
    faHandHoldingDollar,
    faReceipt,
  } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "fontawesome-svelte";

  export let active_name = ""; // dashboard, employee, salary

  let cur_state = true;
</script>

<nav class="side-navbar">
  <div class="logo-container">
    <div class="logo-large">
      <img
        src="static/images/bara_logo_hrzt.svg"
        alt="logo-large"
        height="60"
        width="200px"
      />
    </div>
    <div class="logo-small">
      <img src="static/images/bara_logo_tiny.svg" alt="logo-small" width="30" />
    </div>
  </div>

  <div class="menu-container">
    <div class="nav-item" class:active={active_name === "dashboard"}>
      <a class="nav-link" href="/dashboard" use:link replace>
        <div class="icon-wrap">
          <FontAwesomeIcon icon={faPieChart} />
        </div>
        <span>대쉬보드</span>
      </a>
    </div>
    <div class="nav-item" class:active={active_name === "transaction"}>
      <a class="nav-link" href="/transaction" use:link>
        <div class="icon-wrap">
          <FontAwesomeIcon icon={faReceipt} />
        </div>
        <span>업무현황</span>
      </a>
    </div>
    <div class="nav-item" class:active={active_name === "employee"}>
      <a class="nav-link" href="/employee" use:link>
        <div class="icon-wrap">
          <FontAwesomeIcon icon={faUserGroup} />
        </div>
        <span>직원목록</span>
      </a>
    </div>

    <div class="nav-item" class:active={active_name === "salary"}>
      <a class="nav-link" href="/salary" use:link>
        <div class="icon-wrap">
          <FontAwesomeIcon icon={faHandHoldingDollar} />
        </div>
        <span>급여확인</span>
      </a>
    </div>
  </div>
</nav>

<style lang="scss">
  .side-navbar {
    & {
      position: fixed;
      width: var(--bara-side-navbar-width);
      background-color: var(--bara-side-navbar-background-color);
      min-height: 100vh;
      z-index: 1;
    }

    .logo-container {
      display: flex;
      justify-content: center;
    }

    .logo-large {
      padding: 30px 0px;
      display: flex;
      align-items: center;
      justify-self: center;
      span {
        color: white;
        font-size: 25px;
        margin-left: 15px;
      }
    }

    .logo-small {
      padding: 30px 0px;
      display: none;
    }

    .nav-item {
      font-size: 17px;
      color: var(--bara-side-navbar-vertical-link-color);
      color: inherit;

      &.active .nav-link {
        color: var(--bara-side-navbar-vertical-link-active-color);
      }
      &:not(.active):hover .nav-link {
        color: var(--bara-side-navbar-vertical-link-hover-color);
        transition: 0.5s;
      }

      .nav-link {
        display: flex;
        color: var(--bara-side-navbar-vertical-link-color);
        position: relative;
        padding: 15px 30px;
        .icon-wrap {
          width: 30px;
          text-align: center;
        }
        span {
          margin-left: 15px;
        }
      }
    }
  }

  :global(.container[sidebar-enabled="false"] .side-navbar) {
    & {
      width: var(--bara-side-navbar-small-width);
    }

    .logo-large {
      display: none;
    }
    .logo-small {
      display: block;
    }
    .nav-item:hover {
      background-color: #727cf5;
      z-index: 10;
      width: 200px;
      position: relative;
      box-shadow: var(--bara-side-navbar-box-shadow);
    }

    .nav-item:hover span {
      display: block;
    }
    .nav-link {
      padding-left: 20px;
      padding-right: 20px;
      span {
        display: none;
      }
    }
  }

  @media (max-width: 975px) {
    :global(.container[sidebar-enabled="true"] .side-navbar) {
      & {
        width: var(--bara-side-navbar-small-width);
      }

      .logo-large {
        display: none;
      }
      .logo-small {
        display: block;
      }

      .nav-item {
        &:hover {
          background-color: #727cf5;
          z-index: 10;
          width: 200px;
          position: relative;
          box-shadow: var(--bara-side-navbar-box-shadow);
        }

        &:hover span {
          display: block;
        }
        &:not(.active):hover .nav-link {
          color: var(--bara-side-navbar-vertical-link-hover-color);
          transition: 0.5s;
        }

        .nav-link {
          & {
            padding-left: 20px;
            padding-right: 20px;
          }
          span {
            display: none;
          }
        }

        .nav-link:hover {
          span {
            display: block;
          }
        }
      }
    }

    :global(.container[sidebar-enabled="false"] .side-navbar) {
      display: none;
    }
  }

  @media (max-width: 576px) {
    :global(.container[sidebar-enabled="true"] .side-navbar) {
      display: none;
    }

    :global(.container[sidebar-enabled="false"] .side-navbar) {
      display: block;
    }
  }
</style>
