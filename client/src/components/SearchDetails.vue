<template>
  <div id="SearchDetails" class="col-10">
    <div>
      <h6>Search</h6>

      <dl class="row">
        <dt class="col-6 text-right">Best move: </dt>
        <dd class="col-6">{{ move }}</dd>
      </dl>
      <hr />

      <dl class="row" align-v="center">
        <dt class="col-3 text-right">Evaluation: </dt>
        <dd class="col-3">{{ eval }}</dd>
        <dt class="col-3 text-right">NPS:</dt>
        <dd class="col-3">{{ (nps/1e6).toFixed(2) }} Mn/s</dd>
      </dl>
      <hr />

      <dl class="row" align-v="center">
        <dt class="col-3 text-right">Time: </dt>
        <dd class="col-3">{{ (time/1000).toFixed(2) }}s</dd>
        <dt class="col-3 text-right">Depth/SD:</dt>
        <dd class="col-3">{{ depth }}/{{ seldepth }}</dd>
      </dl>
      <hr />

      <dl class="row" align-v="center">
        <dt class="col-3 text-right">Nodes: </dt>
        <dd class="col-3">{{ (nodes/1e6).toFixed(2) }} M</dd>
        <dt class="col-3 text-right">TB hits:</dt>
        <dd class="col-3">{{ tbhits }}</dd>
      </dl>
      <hr />


      <dl class="row">
        <dt class="col-3 text-right">Principal Variation: </dt>
        <dd class="col-9">
          <span
            v-for="(mv, ix) in pv"
            :key="`${mv}${ix}`">
            {{ (ix % 2) === 0 ? ((ix/2)+1 + '.') : ''}}
            {{ mv }}
          </span>
        </dd>
      </dl>

    </div>
  </div>
</template>

<script>
export default {
  name: 'EngineDetails',
  props: ['move', 'eval', 'nps', 'time', 'depth', 'seldepth', 'nodes', 'tbhits', 'pv'],
};
</script>

<style>

#SearchDetails {
  margin: 0 auto;
  padding: 5px;
  border: 1px solid #dee2e6;
}

#SearchDetails hr {
  margin-top: 8px;
  margin-bottom: 8px;
}

</style>
