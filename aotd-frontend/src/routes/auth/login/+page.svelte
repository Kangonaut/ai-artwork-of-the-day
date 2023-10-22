<script lang="ts">
  import type { ActionData } from "./$types";

  export let form: ActionData;
</script>

<div>
  <h2 class="h2">Login</h2>
  <form method="POST">
    <div
      class="my-10 input-group input-group-divider grid-cols-[auto_1fr_auto]"
    >
      <div class="input-group-shim">Username</div>
      <input
        name="username"
        type="text"
        title="username"
        required
        placeholder="hyper-organce-22"
      />
      <div title="Username already in use.">
        <box-icon type="solid" name="user" color="white" />
      </div>
    </div>

    <div
      class="my-10 input-group input-group-divider grid-cols-[auto_1fr_auto]"
    >
      <div class="input-group-shim">Password</div>
      <input
        name="password"
        type="password"
        title="password"
        required
        placeholder="v3ry s3cure p4ssw0rd 1nd33d!"
      />
      <div title="Password does not fulfill the requirements.">
        <box-icon type="solid" name="key" color="white" />
      </div>
    </div>

    <div class="my-10">
      <button type="submit" class="btn variant-ghost-primary">
        <span>Submit</span>
        <box-icon type="solid" name="rocket" color="white" />
      </button>
    </div>

    {#if form?.error}
      <div class="my-20">
        <div class="card p-4 variant-ghost-error">{form.error}</div>
      </div>
    {/if}
  </form>
</div>
