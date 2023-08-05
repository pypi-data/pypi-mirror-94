<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <ul class="nav nav-tabs">
    <li class="nav-item" v-for="item in items" :key="item.id">
      <span class="nav-link"
            :id="item.id + '_trigger'"
            :data-target="'#' + item.id"
            @click="changeTab(item.id)"
            style="cursor: pointer;">
        <span v-html="item.content"></span>
      </span>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    items: Array,
    tabParam: {
      type: String,
      default: 'tab',
    },
  },
  methods: {
    changeTab(id) {
      const item = this.items.find((item) => item.id === id);
      if (!item) {
        return;
      }

      const url = new URL(window.location);
      const params = new URLSearchParams(url.search);
      params.set(this.tabParam, item.param);
      url.search = params;

      window.history.replaceState(null, null, url);

      $(`#${item.id}_trigger`).tab('show');
    },
  },
  mounted() {
    let currentItem = this.items[0];
    const currentParam = new URLSearchParams(window.location.search).get(this.tabParam);

    for (const item of this.items) {
      if (item.param === currentParam) {
        currentItem = item;
      }
      // Make sure the tab is actually shown before emitting the event.
      $(`#${item.id}_trigger`).on('shown.bs.tab', () => this.$emit('change-tab', item.id));
    }

    $(`#${currentItem.id}_trigger`).tab('show');
  },
};
</script>
