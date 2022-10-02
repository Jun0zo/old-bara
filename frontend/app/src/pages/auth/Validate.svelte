<script>
  import AuthTemplate from "../../templates/AuthTemplate.svelte";
  import BaraCard, { Body } from "~/components/bara-card";
  import { fade, scale } from "svelte/transition";
</script>

<AuthTemplate>
  <div class="card-wrap" in:scale out:fade>
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
          <div>회원님의 메일로 인증버튼이 발송되었습니다. 메일을 확인해보세요!</div>
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

    .content-text {
      font-size: 14px;
      color: #02aef4;
    }

    .content-text:hover {
      cursor: pointer;
      text-decoration: underline;
    }

    .title-wrap {
      padding: 20px;
      margin-bottom: 20px;
    }
  }
</style>
