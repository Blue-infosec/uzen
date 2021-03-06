<template>
  <div>
    <div class="box">
      <BasicForm v-bind:source.sync="source" v-bind:target.sync="target" />
      <hr />
      <SnapshotSearch ref="search" />
      <br />
      <div class="has-text-centered">
        <b-button type="is-light" @click="scan">Scan</b-button>
      </div>
    </div>
    <h2 v-if="hasCount()">
      {{ count }} snapshots found
      <Counter />
    </h2>

    <SnapshotTable v-bind:snapshots="snapshots" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import axios, { AxiosError } from "axios";

import { ErrorData, Snapshot, SearchFilters, TargetTypes } from "@/types";

import BasicForm from "@/components/yara/BasicForm.vue";
import Counter from "@/components/ui/Counter.vue";
import SnapshotSearch from "@/components/snapshots/Search.vue";
import SnapshotTable from "@/components/snapshots/Table.vue";

@Component({
  components: {
    BasicForm,
    Counter,
    SnapshotSearch,
    SnapshotTable
  }
})
export default class YaraForm extends Vue {
  private source: string = "";
  private target: TargetTypes = "body";
  private count: number | undefined = undefined;
  private snapshots: Snapshot[] = [];

  async scan() {
    this.snapshots = [];
    this.count = undefined;

    const loadingComponent = this.$buefy.loading.open({
      container: this.$refs.element
    });

    const params = (this.$refs.search as SnapshotSearch).filtersParams();

    try {
      const response = await axios.post<Snapshot[]>(
        "/api/yara/scan",
        {
          source: this.source,
          target: this.target
        },
        { params: params }
      );

      loadingComponent.close();

      this.snapshots = response.data;
      this.count = this.snapshots.length;
    } catch (error) {
      loadingComponent.close();

      const data = error.response.data as ErrorData;
      alert(data.detail);
    }
  }

  hasCount(): boolean {
    return this.count !== undefined;
  }
}
</script>
