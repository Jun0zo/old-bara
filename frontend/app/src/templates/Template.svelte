<script>
  import SideNavbar from "~/components/SideNavbar.svelte";
  import Navbar from "~/components/Navbar.svelte";
  import { sidebar_enabled_ } from "~/store";
  export let nav_info;

  let sidebar_enabled = "";

  sidebar_enabled_.subscribe((value) => {
    sidebar_enabled = value;
  });
</script>

<div class="container" sidebar-enabled={sidebar_enabled}>
  <SideNavbar active_name={nav_info.active_name} />
  <div class="content-page">
    <Navbar />
    <div class="title">{nav_info.title_name}</div>
    <slot />
  </div>
</div>

<style lang="scss">
  .content-page {
    padding: 70px 30px;
    flex: 1;
    box-sizing: border-box;
    width: calc(100% - var(--bara-side-navbar-width));
    margin-left: var(--bara-side-navbar-width);
    .title {
      padding: 20px 0px;
      font-size: 18px;
      font-weight: 700;
    }
  }

  :global(.container[sidebar-enabled="false"]) {
    .content-page {
      width: calc(100% - var(--bara-side-navbar-small-width));
      margin-left: var(--bara-side-navbar-small-width);
    }
  }

  @media (max-width: 975px) {
    .content-page {
      width: calc(100% - var(--bara-side-navbar-small-width));
      margin-left: var(--bara-side-navbar-small-width);
    }

    :global(.container[sidebar-enabled="false"]) {
      .content-page {
        width: 100%;
        margin-left: 0px;
      }
    }
  }

  @media (max-width: 576px) {
    .content-page {
      width: 100%;
      margin-left: 0px;
    }
  }
</style>
