<script>
  import Card, { Content } from "@smui/card";
</script>

<Card style="height:100%;" {...$$restProps}>
  <slot />
</Card>

<style>
  :global(.mdc-card) {
    border-radius: var(--bara-card-border-radius);
    box-shadow: var(--bara-card-box-shadow);
  }
</style>
