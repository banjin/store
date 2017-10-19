<!--<template>-->
  <!--<div id="app">-->
    <!--<img class="logo" src="./assets/logo.png">-->
    <!--<hello></hello>-->
    <!--<p>-->
      <!--Welcome to your Vue.js app!-->
    <!--</p>-->
    <!--<p>-->
      <!--To get a better understanding of how this boilerplate works, check out-->
      <!--<a href="http://vuejs-templates.github.io/webpack" target="_blank">its documentation</a>.-->
      <!--It is also recommended to go through the docs for-->
      <!--<a href="http://webpack.github.io/" target="_blank">Webpack</a> and-->
      <!--<a href="http://vuejs.github.io/vue-loader/" target="_blank">vue-loader</a>.-->
      <!--If you have any issues with the setup, please file an issue at this boilerplate's-->
      <!--<a href="https://github.com/vuejs-templates/webpack" target="_blank">repository</a>.-->
    <!--</p>-->
    <!--<p>-->
      <!--You may also want to checkout-->
      <!--<a href="https://github.com/vuejs/vue-router/" target="_blank">vue-router</a> for routing and-->
      <!--<a href="https://github.com/vuejs/vuex/" target="_blank">vuex</a> for state management.-->
      <!--<button v-on:click='print'>点击</button>-->
      <!--<br>-->
    <!--</p>-->
  <!--</div>-->
<!--</template>-->
    <template>
      <div class="temp-input-box m-t-20">
        <span>选择模板文件:</span>
      <span class="ys-file-box d-i-b">
        <span class="file-name d-i-b">{{fileName}}</span>
        <span class="ys-file-btn d-i-b" @click="selFileFunc()">
          <i class="glyphicon glyphicon-folder-close"></i>选择文件
          <div class="form-group d-none">
            <form enctype="multipart/form-data" method="post">
              <input id="fileUploadFile" type="file" @change="bindFile" class="form-control" multiple="">
            </form>
          </div>
        </span>
      </span>
      </div>
      <div style="width:580px;" class="m-t-20">
        <p class="fRight"><button class="ys-btn" @click="uploadThisFile">确认添加</button></p>
         <button @click="down_table">下载</button>
      </div>
      <br>
      <br/>
      <a href="change_work_table_name.csv" download="">下载</a>
      <div id="websocket">
        <p>{{ message }}</p>
        <input v-model="message">
        <button v-on:click="reverseMessage">Reverse Message</button>
      </div>
    </template>


<script>
import Hello from './components/Hello'


export default ({
   data() {
      return {
        fileUploadFormData:new FormData(),//文件上传
        fileName:"",
        message:'HELLO',
        ws: null,
        work_table_id:0
      }
    },
  methods: {
    selFileFunc(){
        $("#fileUploadFile").click()
      },
    bindFile(e){
        e.preventDefault();
        this.fileUploadFormData.append('csv_file', e.target.files[0]);
        this.fileName=e.target.files[0].name;
      },
    down_table(){
      this.$http.post('/down/').then(function (response) {
        if (response.status == 200) {
          console.log('下载成功')
          this.$root.alertSuccess = true;
      }
    });
    },
    reverseMessage(){
		  		// Emit the server side
          var ws = new WebSocket("ws://" + '127.0.0.1:8000' + "/lower_case");
          console.log('WebSocket open');
          window.s = ws
          window.s.send(this.message);
//		  		this.$socket.emit("add", { a: 5, b: 3 });
			},
    add() {
		  		// Emit the server side
		  		this.$socket.emit("add", { a: 5, b: 3 });
			},
    uploadThisFile(e){
      e.preventDefault();
      if (this.fileUploadFormData.file == undefined) this.fileUploadFormData.append('file', '');
      this.$http.post('/book12/', this.fileUploadFormData).then(function (response) {
        if (response.status == 200) {
          console.log('上传成功')
          this.$root.alertSuccess = true;
        } else {
          this.$root.alertError = true;
          console.log('failed')
          console.log(response)
        }
        this.$root.errorMsg = response.data.msg;
      }, function (data) {
        //error handling here
      });
    },
    socket: {
			// Prefix for event names
			// prefix: "/counter/",

			// If you set `namespace`, it will create a new socket connection to the namespace instead of `/`
			// namespace: "/counter",

			events: {

				// Similar as this.$socket.on("changed", (msg) => { ... });
				// If you set `prefix` to `/counter/`, the event name will be `/counter/changed`
				//
				changed(msg) {
					console.log("Something changed: " + msg);
				}

				/* common socket.io events
				connect() {
					console.log("Websocket connected to " + this.$socket.nsp);
				},

				disconnect() {
					console.log("Websocket disconnected from " + this.$socket.nsp);
				},

				error(err) {
					console.error("Websocket error!", err);
				}
				*/

			}
		}
  },
  components:
   {
    Hello
  }
})

</script>

<style>
html {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

#app {
  color: #2c3e50;
  margin-top: -100px;
  max-width: 600px;
  font-family: Source Sans Pro, Helvetica, sans-serif;
  text-align: center;
}

#app a {
  color: #42b983;
  text-decoration: none;
}

.logo {
  width: 100px;
  height: 100px
}
</style>
