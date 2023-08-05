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
  <dynamic-pagination :endpoint="endpoint"
                      :placeholder="placeholder"
                      :per-page="perPage"
                      :enable-filter="enableFilter"
                      :filter-placeholder="filterPlaceholder"
                      :filter-param="filterParam">
    <template #default="paginationProps">
      <div class="row">
        <div class="col-lg-4">
          <p>
            <strong>{{ title }}</strong>
            <span class="badge badge-pill badge-light text-muted border border-muted">{{ paginationProps.total }}</span>
          </p>
        </div>
        <div class="col-lg-8">
          <slot></slot>
        </div>
      </div>
      <card-deck :items="paginationProps.items">
        <template #default="props">
          <div class="card-body pt-3 pb-1">
            <a :href="props.item._links.view" class="stretched-link">
              <p>
                <span class="badge badge-primary font-weight-normal float-right">
                  {{ props.item.type | capitalize }}
                </span>
                <strong>{{ props.item.title }}</strong>
                <br>
                <small>@{{ props.item.identifier }}</small>
              </p>
            </a>
          </div>
          <div class="card-footer bg-white py-1">
            <small class="text-muted">
              {{ i18n.t('misc.lastModified') }} <from-now :timestamp="props.item.last_modified"></from-now>
            </small>
          </div>
        </template>
      </card-deck>
    </template>
  </dynamic-pagination>
</template>

<script>
export default {
  props: {
    title: String,
    placeholder: String,
    endpoint: String,
    perPage: {
      type: Number,
      default: 6,
    },
    enableFilter: {
      type: Boolean,
      default: false,
    },
    filterPlaceholder: {
      type: String,
      default: 'Filter',
    },
    filterParam: {
      type: String,
      default: '&filter',
    },
  },
};
</script>
