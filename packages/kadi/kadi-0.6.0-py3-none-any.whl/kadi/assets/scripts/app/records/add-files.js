/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import CanvasPainter from 'scripts/lib/components/CanvasPainter.vue';
import UploadManager from 'scripts/lib/components/UploadManager.vue';
import WorkflowEditor from 'scripts/lib/components/WorkflowEditor.vue';

new Vue({
  el: '#vm',
  components: {
    CanvasPainter,
    UploadManager,
    WorkflowEditor,
  },
  data: {
    currentTab: 'upload-files',
    originDrawing: 'drawing',
    originWorkflow: 'workflow',
    currentDrawing: null,
    currentWorkflow: null,
    drawingUrl: null,
    workflowUrl: null,
    filenameDrawing: '',
    filenameWorkflow: '',
    unsavedChangesDrawing: false,
    unsavedChangesWorkflow: false,
    renderDrawingTab: false,
    renderWorkflowTab: false,
    uploadingDrawing: false,
    uploadingWorkflow: false,
  },
  methods: {
    changeTab(id) {
      // If we render the drawing or workflow components before they are shown, their size cannot be initialized
      // correctly.
      if (id === 'upload-drawing') {
        this.renderDrawingTab = true;
      } else if (id === 'upload-workflow') {
        this.renderWorkflowTab = true;
      }
      this.currentTab = id;
    },
    uploadCompleted(file, origin) {
      if (origin === this.originDrawing) {
        this.currentDrawing = file;
        this.updateUrl(file);
      } else if (origin === this.originWorkflow) {
        this.currentWorkflow = file;
        this.updateUrl(file);
      }

      this.updateUploadState(origin);
    },
    uploadCanceled(upload, origin) {
      this.updateUploadState(origin);
    },
    updateUrl(file) {
      // Update the current (or last uploaded) file in the URL as well.
      const url = new URL(window.location);
      const params = new URLSearchParams(url.search);
      params.set('file', file.id);
      url.search = params;

      window.history.replaceState(null, null, url);
    },
    updateUploadState(origin) {
      if (origin === this.originDrawing) {
        this.uploadingDrawing = false;
      } else if (origin === this.originWorkflow) {
        this.uploadingWorkflow = false;
      }
    },
    uploadFile(currentFile, file, origin) {
      // When trying to replace a file that is currently being edited, we skip the confirmation for replacing existing
      // files.
      this.$refs.uploadManager.addFile(file, currentFile && currentFile.name === file.name, origin);
    },
    checkFile(currentFile, filename, callback) {
      if (currentFile && currentFile.name === filename) {
        axios.get(currentFile._links.self)
          .then((response) => {
            // Check if the content of the current file has changed since loading or last uploading it by just comparing
            // the checksums.
            if (currentFile.checksum !== response.data.checksum) {
              if (confirm(i18n.t('warning.fileChanged'))) {
                callback();
              }
            } else {
              callback();
            }
          });
      } else {
        callback();
      }
    },
    dataURLtoFile(dataurl, filename) {
      const bstr = atob(dataurl.split(',')[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);

      while (n) {
        u8arr[n - 1] = bstr.charCodeAt(n - 1);
        n -= 1;
      }
      return new File([u8arr], filename);
    },
    saveDrawing(canvas) {
      let filename = this.filenameDrawing;
      if (!filename.endsWith('.png')) {
        filename += '.png';
      }

      const _uploadImage = () => {
        const file = this.dataURLtoFile(canvas.toDataURL(), filename);
        this.uploadFile(this.currentDrawing, file, this.originDrawing);
        this.uploadingDrawing = true;
        this.unsavedChangesDrawing = false;
      };

      this.checkFile(this.currentDrawing, filename, _uploadImage);
    },
    saveWorkflow(editor) {
      let filename = this.filenameWorkflow;
      if (!filename.endsWith('.flow')) {
        filename += '.flow';
      }

      const _uploadWorkflow = () => {
        const file = new File([JSON.stringify(editor.toJSON())], filename);
        this.uploadFile(this.currentWorkflow, file, this.originWorkflow);
        this.uploadingWorkflow = true;
        this.unsavedChangesWorkflow = false;
      };

      this.checkFile(this.currentWorkflow, filename, _uploadWorkflow);
    },
  },
  mounted() {
    if (kadi.js_resources.current_file_endpoint) {
      axios.get(kadi.js_resources.current_file_endpoint)
        .then((response) => {
          const data = response.data;
          if (['image/png', 'image/jpeg'].includes(data.magic_mimetype)) {
            this.currentDrawing = data;
            this.filenameDrawing = data.name;
            this.drawingUrl = data._links.download;
            this.$refs.navTabs.changeTab('upload-drawing');
          } else if (data.magic_mimetype === 'application/x-flow+json') {
            this.currentWorkflow = data;
            this.filenameWorkflow = data.name;
            this.workflowUrl = data._links.download;
            this.$refs.navTabs.changeTab('upload-workflow');
          }
        })
        .catch((error) => kadi.alert(i18n.t('error.loadFile'), {xhr: error.request}));
    }
  },
});
