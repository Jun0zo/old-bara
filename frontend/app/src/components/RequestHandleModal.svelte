<script>
  import Dialog, { Title, Content, Actions, Header } from "@smui/dialog";
  import Button, { Label } from "@smui/button";
  import { request_handle_modal_open_ } from "~/store";
  import { get } from "svelte/store";

  let open = get(request_handle_modal_open_);
  request_handle_modal_open_.subscribe((value) => {
    open = value;
  });

//   $: {
//     request_handle_modal_open_.update(value => open);
//   }
</script>

<Dialog bind:open>
  <Header>
    <Title>업무현황 추가</Title>
  </Header>
  <Content>
    <svg
      class="checkmark success"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 52 52"
      ><circle
        class="checkmark_circle_success"
        cx="26"
        cy="26"
        r="25"
        fill="none"
      /><path
        class="checkmark_check"
        fill="none"
        d="M14.1 27.2l7.1 7.2 16.7-16.8"
        stroke-linecap="round"
      /></svg
    >

    <svg
      class="checkmark error"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 52 52"
      ><circle
        class="checkmark_circle_error"
        cx="26"
        cy="26"
        r="25"
        fill="none"
      /><path
        class="checkmark_check"
        stroke-linecap="round"
        fill="none"
        d="M16 16 36 36 M36 16 16 36
"
      /></svg
    >
  </Content>
  <Actions>
    <Button>
      <Label>확인</Label>
    </Button>
  </Actions>
</Dialog>

<style lang="scss">
  $color-success: #00c851;
  $color-error: #ff4444;
  $stroke-width: 5px;
  $size: 150px;
  $checkmark-color: white;

  .checkmark_circle_success {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: $stroke-width;
    stroke-miterlimit: 10;
    stroke: $color-success;
    animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
  }

  .checkmark_circle_error {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: $stroke-width;
    stroke-miterlimit: 10;
    stroke: $color-error;
    animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
  }

  .checkmark {
    width: $size;
    height: $size;
    border-radius: 50%;
    display: block;
    stroke-width: $stroke-width;
    stroke: $checkmark-color;
    stroke-miterlimit: 10;
    margin: 10% auto;
    &.success {
      box-shadow: inset 0px 0px 0px $color-success;
      animation: fillsuccess 0.4s ease-in-out 0.4s forwards,
        scale 0.3s ease-in-out 0.9s both;
    }
    &.error {
      box-shadow: inset 0px 0px 0px $color-error;
      animation: fillerror 0.4s ease-in-out 0.4s forwards,
        scale 0.3s ease-in-out 0.9s both;
    }
  }

  .checkmark_check {
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.9s forwards;
  }

  .progress {
    transform: rotate(-90deg);
    stroke: black;
  }

  .progress circle {
    stroke-dasharray: 130;
    stroke-dashoffset: 130;
    animation: dash 1.5s infinite;
  }

  @keyframes dash {
    50% {
      stroke-dashoffset: 0;
    }
    100% {
      stroke-dashoffset: -130;
    }
  }

  .progress {
    position: absolute;
    top: 5%;
    left: 5%;

    &.progress--thin {
      left: auto;
      right: 5%;
    }
  }

  @keyframes stroke {
    100% {
      stroke-dashoffset: 0;
    }
  }
  @keyframes scale {
    0%,
    100% {
      transform: none;
    }
    50% {
      transform: scale3d(1.1, 1.1, 1);
    }
  }
  @keyframes fillsuccess {
    100% {
      box-shadow: inset 0px 0px 0px $size/2 $color-success;
    }
  }

  @keyframes fillerror {
    100% {
      box-shadow: inset 0px 0px 0px $size/2 $color-error;
    }
  }
</style>
