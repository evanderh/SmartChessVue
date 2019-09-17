<template>
  <div id="EngineDetails" class="col-10">
    <h6>Engine</h6>
    <div>
      <!-- Engine name -->
      <dl class="row">
        <dt class="col-3">Name: </dt>
        <dd v-if="key" class="col-9">
          {{ name }}
        </dd>
        <dd v-else class="col-9">
          Loading...
        </dd>
      </dl>
      <!-- Engine link -->
      <dl class="row">
        <dt class="col-3">Link: </dt>
        <dd v-if="key" class="col-9">
          <b-link :href="details[key].link">
            <small>{{ details[key].link }}</small>
          </b-link>
        </dd>
        <dd v-else class="col-9">
          <small>Loading...</small>
        </dd>
      </dl>
      <!-- Engine description -->
      <dl class="row">
        <dt class="col-3">Description: </dt>
        <dd v-if="key" class="col-9">
          <small>{{ details[key].description }}</small>
        </dd>
        <dd v-else class="col-9">
          <small>Loading...</small>
        </dd>
      </dl>
    </div>
    <!-- Loading -->
  </div>
</template>

<script>
export default {
  name: 'EngineDetails',
  props: {
    name: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      details: {
        Lozza: {
          description: `A simple Javascript UCI chess engine rated about 2400 on
            CCRL. Lozza is a traditional engine with an evaluation function based
            on Fabien Letouzey's Fruit.`,
          link: 'https://github.com/op12no2/lozza',
        },
      },
    };
  },
  computed: {
    key() {
      return this.name.split(' ').shift();
    },
  },
};
</script>

<style>

#EngineDetails {
  margin: 15px auto 0 auto;
  padding: 5px;
  border: 1px solid #dee2e6;
}

</style>
