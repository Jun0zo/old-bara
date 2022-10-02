<script>
  import { Router, Route } from "svelte-routing";

  import Dashboard from "~/pages/Dashboard.svelte";
  import Employee from "~/pages/Employee.svelte";
  import Transaction from "~/pages/Transaction.svelte";
  import Salary from "~/pages/Salary.svelte";
  import Login from "~/pages/auth/Login.svelte";
  import Register from "~/pages/auth/Register.svelte";
  import Validate from "~/pages/auth/Validate.svelte";
  import VerifyEmail from "~/pages/auth/VerifyEmail.svelte";

  export let url = "";
</script>

<Router {url}>
  <main>
    <Route path="/" component={Login} />
    <Route path="/dashboard" component={Dashboard} />
    <Route path="/employee" component={Employee} />
    <Route path="/transaction" component={Transaction} />
    <Route path="/salary" component={Salary} />
    <Route path="/login" component={Login} />
    <Route path="/register" component={Register} />
    <Route path="/validate" component={Validate} />
    <Route path="/verify-email/:tocken_id" component={VerifyEmail} />
  </main>
</Router>

<style>
  main {
    /* padding: 0px var(--bara-main-padding); */
    /* width: 100%; */
    background-color: var(--bara-body-bg);
    color: var(--bara-body-color);
    font: var(--bara-body-font-family);
    height: 100%;
  }
</style>
