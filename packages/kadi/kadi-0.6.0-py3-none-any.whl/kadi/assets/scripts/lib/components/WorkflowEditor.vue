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
  <div>
    <div class="card editor-container" :class="{'bg-light': !editable}" ref="editorContainer">
      <div class="editor-toolbar" ref="editorToolbar">
        <button title="Reset view" type="button" class="btn btn-link text-muted" @click="resetView">
          <i class="fas fa-eye"></i>
        </button>
        <button title="Toggle fullscreen" type="button" class="btn btn-link text-muted" @click="toggleFullscreen">
          <i class="fas fa-expand"></i>
        </button>
        <button title="Reset editor" type="button" class="btn btn-link text-muted" v-if="editable" @click="resetEditor">
          <i class="fas fa-broom"></i>
        </button>
      </div>
      <div ref="editor"></div>
    </div>
    <slot :editor="editor"></slot>
  </div>
</template>

<style scoped>
.editor-container {
  border: 1px solid #ced4da;
}

.editor-toolbar {
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>

<script>
import 'regenerator-runtime';
import Rete from 'rete';
import AreaPlugin from 'rete-area-plugin';
import ConnectionPlugin from 'rete-connection-plugin';
import ConnectionMasteryPlugin from 'rete-connection-mastery-plugin';
import ContextMenuPlugin from 'rete-context-menu-plugin';
import VueRenderPlugin from 'rete-vue-render-plugin';

import WorkflowEditor from 'scripts/lib/workflows/core';
import Menu from 'scripts/lib/workflows/Menu.vue';

import IntComponent from 'scripts/lib/workflows/components/IntComponent';
import FloatComponent from 'scripts/lib/workflows/components/FloatComponent';
import StringComponent from 'scripts/lib/workflows/components/StringComponent';
import BoolComponent from 'scripts/lib/workflows/components/BoolComponent';
import FileOutComponent from 'scripts/lib/workflows/components/FileOutComponent';
import FileInComponent from 'scripts/lib/workflows/components/FileInComponent';
import UserInputTextComponent from 'scripts/lib/workflows/components/UserInputTextComponent';
import UserInputFileComponent from 'scripts/lib/workflows/components/UserInputFileComponent';
import UserInputCropImagesComponent from 'scripts/lib/workflows/components/UserInputCropImagesComponent';
import CustomComponent from 'scripts/lib/workflows/components/CustomComponent';

import scalardata2image from 'scripts/lib/workflows/xml/scalardata2image';
import fieldtransformData from 'scripts/lib/workflows/xml/fieldtransform';
import volumeData from 'scripts/lib/workflows/xml/volume';
import infile2simgeoData from 'scripts/lib/workflows/xml/infile2simgeo';
import toolcombineData from 'scripts/lib/workflows/xml/toolcombine';
import StartReportData from 'scripts/lib/workflows/xml/StartReport';
import TextReportData from 'scripts/lib/workflows/xml/TextReport';
import EndReportData from 'scripts/lib/workflows/xml/EndReport';
import ImageJMacroData from 'scripts/lib/workflows/xml/ImageJMacro';
import mkdirData from 'scripts/lib/workflows/xml/systemMkdir';

import 'styles/workflows/workflow-editor.scss';

export default {
  data() {
    return {
      editor: null,
      engine: null,
      area: null,
      unsavedChanges_: false,
      resizeHandler: null,
      beforeunloadHandler: null,
    };
  },
  props: {
    version: {
      type: String,
      default: 'kadi@0.1.0',
    },
    editable: {
      type: Boolean,
      default: true,
    },
    workflowUrl: {
      type: String,
      default: null,
    },
    unsavedChanges: {
      type: Boolean,
      default: false,
    },
    isRendered: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    workflowUrl() {
      this.loadWorkflow();
    },
    unsavedChanges() {
      this.unsavedChanges_ = this.unsavedChanges;
    },
    unsavedChanges_() {
      this.$emit('unsaved-changes', this.unsavedChanges_);
    },
    isRendered() {
      this.resizeView(false);
    },
  },
  methods: {
    isFullscreen() {
      return document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
    },
    resetView() {
      this.area.zoomAt(this.editor);
    },
    toggleFullscreen() {
      if (this.isFullscreen()) {
        document.exitFullscreen();
      } else {
        this.$refs.editorContainer.requestFullscreen();
      }
    },
    resetEditor() {
      if (!confirm('Are you sure you want to reset the editor?')) {
        return;
      }
      this.editor.clear();
      this.unsavedChanges_ = false;
    },
    resizeView(resetView = true) {
      // In case the component is not marked as rendered from the outside we do not attempt to resize it.
      if (!this.isRendered) {
        return;
      }

      const width = this.$refs.editorContainer.getBoundingClientRect().width;
      if (this.isFullscreen()) {
        this.$refs.editorContainer.style.height = '100vh';
      } else {
        this.$refs.editorContainer.style.height = `${Math.round(window.innerHeight / window.innerWidth * width)}px`;
      }
      this.editor.view.resize();

      if (resetView) {
        this.resetView();
      }
    },
    loadWorkflow() {
      if (!this.workflowUrl) {
        return;
      }

      axios.get(this.workflowUrl)
        .then((response) => {
          // Catch errors in the custom fromJSON function as well.
          try {
            this.editor.fromJSON(response.data)
              .then((success) => {
                if (!success) {
                  kadi.alert('Could not fully reconstruct workflow.', {type: 'warning'});
                }
              })
              .catch((error) => {
                console.error(error);
                kadi.alert('Error parsing workflow data.');
              })
              .finally(() => this.resetView());
          } catch (e) {
            kadi.alert('Error parsing workflow data.');
          }
        });
    },
  },
  mounted() {
    // Disable some events if the editor is not editable.
    if (!this.editable) {
      let handler = (e) => {
        if (!Array.from(this.$refs.editorToolbar.getElementsByTagName('*')).includes(e.target)) {
          e.preventDefault();
          e.stopPropagation();
        }
      };
      this.$refs.editorContainer.addEventListener('click', handler, {capture: true});

      handler = (e) => {
        if (e.target !== this.$refs.editor) {
          e.preventDefault();
          e.stopPropagation();
        }
      };
      this.$refs.editorContainer.addEventListener('pointerdown', handler, {capture: true});
      this.$refs.editorContainer.addEventListener('pointerup', handler, {capture: true});

      handler = (e) => {
        e.preventDefault();
        e.stopPropagation();
      };
      this.$refs.editorContainer.addEventListener('dblclick', handler, {capture: true});
      this.$refs.editorContainer.addEventListener('contextmenu', handler, {capture: true});
    }

    // Initialize the editor and its plugins.
    this.editor = new WorkflowEditor(this.version, this.$refs.editor);
    this.engine = new Rete.Engine(this.version);
    this.area = AreaPlugin;

    this.editor.use(AreaPlugin);
    this.editor.use(ConnectionPlugin);
    this.editor.use(VueRenderPlugin);
    this.editor.use(ConnectionMasteryPlugin);
    this.editor.use(ContextMenuPlugin, {
      vueComponent: Menu,
      searchBar: false,
      delay: 10,
      items: {
        'Debug': {
          /* eslint-disable no-console */
          'Dump JSONflow': () => console.info(this.editor.toJSON()),
          'Dump JSONrete': () => console.info(this.editor.toJSONrete()),
          /* eslint-enable no-console */
        },
      },
      allocate(component) {
        if (component.componentType === 'ToolNode') {
          return ['Tool'];
        } else if (component.componentType === 'InputOutput') {
          return ['Input/Output'];
        } else if (component.componentType === 'PromptNode') {
          return ['Prompt'];
        }
        return ['Source'];
      },
      rename(component) {
        return component.name;
      },
    });

    // Register all components and sockets.
    const numSocket = new Rete.Socket('num');
    const strSocket = new Rete.Socket('str');
    const flagSocket = new Rete.Socket('bool');
    const depSocket = new Rete.Socket('dep');

    const anyTypeSocket = new Rete.Socket('any');
    anyTypeSocket.combineWith(numSocket);
    anyTypeSocket.combineWith(strSocket);
    anyTypeSocket.combineWith(flagSocket);

    const intComponent = new IntComponent(numSocket);
    const floatComponent = new FloatComponent(numSocket);
    const strComponent = new StringComponent(strSocket);
    const boolComponent = new BoolComponent(flagSocket);
    const fileOutComponent = new FileOutComponent(strSocket, flagSocket, depSocket, anyTypeSocket);
    const fileInComponent = new FileInComponent(strSocket, depSocket, anyTypeSocket);
    const userInputTextComponent = new UserInputTextComponent(strSocket, depSocket);
    const userInputFileComponent = new UserInputFileComponent(strSocket, depSocket);
    const userInputCropImagesComponent = new UserInputCropImagesComponent(strSocket, depSocket);

    const customComponentSockets = [numSocket, strSocket, flagSocket, depSocket, anyTypeSocket];
    const customComponent = new CustomComponent(scalardata2image, ...customComponentSockets);
    const fieldtransform = new CustomComponent(fieldtransformData, ...customComponentSockets);
    const volume = new CustomComponent(volumeData, ...customComponentSockets);
    const infile2simgeo = new CustomComponent(infile2simgeoData, ...customComponentSockets);
    const toolcombine = new CustomComponent(toolcombineData, ...customComponentSockets);
    const StartReport = new CustomComponent(StartReportData, ...customComponentSockets);
    const TextReport = new CustomComponent(TextReportData, ...customComponentSockets);
    const EndReport = new CustomComponent(EndReportData, ...customComponentSockets);
    const ImageJMacro = new CustomComponent(ImageJMacroData, ...customComponentSockets);
    const mkdir = new CustomComponent(mkdirData, ...customComponentSockets);

    [
      intComponent,
      floatComponent,
      strComponent,
      boolComponent,
      fileOutComponent,
      fileInComponent,
      userInputTextComponent,
      userInputFileComponent,
      userInputCropImagesComponent,
      customComponent,
      fieldtransform,
      volume,
      infile2simgeo,
      toolcombine,
      StartReport,
      TextReport,
      EndReport,
      ImageJMacro,
      mkdir,
    ].forEach((c) => {
      this.editor.register(c);
      this.engine.register(c);
    });

    // Register custom editor events.
    this.editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async() => {
      // This flag is set when calling fromJSON, in which case we can ignore the events.
      if (this.editor.silent) {
        return;
      }

      await this.engine.abort();
      await this.engine.process(this.editor.toJSONrete());
    });

    // TODO: Needs another event when changing controls (could propably be done easiest in a custom node).
    this.editor.on('nodecreated noderemoved connectioncreated connectionremoved nodetranslated', () => {
      if (!this.editor.silent) {
        this.unsavedChanges_ = true;
      }
    });

    this.editor.on('click', () => {
      this.editor.selected.clear();
      this.editor.nodes.map((n) => n.update());
    });

    this.editor.on('zoom', ({source}) => {
      return source !== 'dblclick';
    });

    // Finalize initialization.
    this.resizeView();
    this.loadWorkflow();

    this.resizeHandler = window.addEventListener('resize', this.resizeView);
    /* eslint-disable consistent-return */
    this.beforeunloadHandler = window.addEventListener('beforeunload', (e) => {
      if (this.unsavedChanges_) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
    });
    /* eslint-enable consistent-return */
  },
  beforeDestroy() {
    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler);
    }
    if (this.beforeunloadHandler) {
      window.removeEventListener('beforeunload', this.beforeunloadHandler);
    }
  },
};
</script>
