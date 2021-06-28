<template>
  <!-- click.self表示只影响自身标签，不会影响下面的子标签 -->
  <div id="login" @click.self="hideSelf">
    <div id="loginbox">
      <div class="form">
        <div class="item">
          <div class="span">用户名：</div>
          <input v-model="username" type="text" placeholder="输入用户名" />
        </div>
        <div class="item">
          <div class="span">密码：</div>
          <input v-model="password" type="text" placeholder="输入密码" />
        </div>
        <div v-if="target == 2" class="item">
          <div class="span">重复密码：</div>
          <input v-model="password2" type="text" placeholder="再次输入密码" />
        </div>
        <button v-if="target == 1" @click="toLogin">登录</button>
        <button v-if="target == 2" @click="toRegister">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
export default {
  name: "LoginBox",
  props: ["target"],
  data() {
    return {
      username: "",
      password: "",
      password2: "",
    };
  },
  mounted() {
    console.log(this.target);
  },
  methods: {
    hideSelf() {
      this.$emit("hideBox");
    },
    //注册
    toRegister() {
      var username = this.username;
      var password = this.password;
      var password2 = this.password2;
      console.log(username, password, password2);
      if (username.length > 0 && password.length > 0 && password2.length > 0) {
        if (password != password2) {
          alert("密码两次输入不同");
        } else {
          axios({
            url: "http://127.0.0.1:9000/register/",
            data: Qs.stringify({
              username,
              password,
              password2,
            }),
            method: "post",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }).then((res) => {
            console.log(res);
            switch (res.data) {
                case 'same':
                    alert('存在同名用户')
                    break
                default:
                    break;
            }
          });
        }
      }else{
          alert('缺少必填项')
      }
    },
    //登录
    toLogin() {
      console.log(this.username, this.password);
      var username = this.username;
      var password = this.password;
      if (username.length > 0 && password.length > 0) {
        axios({
          url: "http://127.0.0.1:9000/login/",
          data: Qs.stringify({
            username,
            password,
          }),
          method: "post",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }).then((res) => {
          console.log(res);
          switch (res.data) {
            case "none":
              alert("用户名不存在");
              break;
            case "pwderr":
              alert("密码错误");
              break;
            default:
              console.log(res.data.token);
              alert("登录成功");
              break;
          }
        });
      } else {
        alert("用户名或密码不能为空");
      }
    },
  },
};
</script>

<style>
#login {
  position: absolute;
  top: 0;
  width: 700px;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #00000020;
}
#loginbox {
  width: 300px;
  height: 300px;
  border: 10px solid #000;
  background: #00000090;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
}
#loginbox .form .item {
  font-weight: 700;
  margin: 10px;
  margin: 10px auto;
}
#loginbox .form .item .span {
  float: left;
  width: 80px;
}
</style>