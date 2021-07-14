<template>
  <div id="home">
    <div>
      <button v-if="loginType==false" @click="showLoginRegisterBox(1)">登录</button>
      <button v-if="loginType==false" @click="showLoginRegisterBox(2)">注册</button>
      <button v-if="loginType" @click="toHome">首页</button>
      <button v-if="loginType" @click="toUserinfo">个人中心</button>
      <button v-if="loginType" @click="showLoginRegisterBox(3)">修改</button>
      <div class="header">
        <h1>{{siteinfo.sitename}}</h1>
        <img :src="siteinfo.logo" alt="" />
      </div>

      <hr />
      <div class="content">
        <div class="menu">
          <div v-for="item in menuList" :key="item.id" class="item">
            <div
              v-if="item.id == choosed"
              style="background: #777777; color: #ffffff"
            >
              <a style="color: #fff">{{
                item.text
              }}</a>
            </div>
            <div v-else style="" @click="chooseMenu(item.id)">
              <a style="color: #000">{{
                item.text
              }}</a>
            </div>
          </div>
        </div>
        <div class="userlist">
          <p>{{choosed_text}}</p>
          <hr />
          <router-view @hideBox="hideLoginRegisterBox" @changeUI="changeLoginType"/>
        </div>
      </div>
      <hr />
    </div>
    <LoginBox v-if="boxtarget" :target="boxtarget" @hideBox="hideLoginRegisterBox"></LoginBox>
    <div class="foot">Copyright gf</div>
  </div>
</template>

<script>
import axios from "axios";
import LoginBox from "../src/components/LoginBox"
export default {
  components:{
    LoginBox
  },
  data() {
    return {
      choosed: 1,
      choosed_text:'Django后端',
      menuList: [],
      boxtarget: 0,
      siteinfo:{},
      loginType:false,
    };
  },
  mounted() {
    try {
      if (window.localStorage.getItem('token').length>0) {
      this.loginType = true
    }
    } catch (error) {
      console.log(error)
    }
    
    this.getMenuList();
  },
  methods: {
    toHome(){
      this.$router.push({path:'/'})
    },
    toUserinfo(){
      this.$router.push({path:'/userinfo'})
    },
    //获取分类列表
    getMenuList() {
      console.log("开始获取分类");
      axios({
        url: "http://127.0.0.1:9000/get-menu-list/",
        type: "json",
        method: "get",
      }).then((res) => {
        console.log(res);
        this.menuList = res.data.menu_data;
        this.siteinfo = res.data.siteinfo;
      });
    },
    chooseMenu(id) {
      console.log(id);
      this.choosed = id;
      for (let index = 0; index < this.menuList.length; index++) {
        if (id==this.menuList[index].id) {
          this.choosed_text=this.menuList[index].text
        }        
      }
      //进行id传参跳转
      this.$router.push({path:'/',query:{menuId:id}})
    },
    //展示登录注册框体
    showLoginRegisterBox(value) {
      this.boxtarget=value
    },
    //隐藏登录注册框体
    hideLoginRegisterBox() {
      this.boxtarget=0
    },
    //修改登录状态
    changeLoginType(bool) {
      this.loginType = bool
    }
  },
};
</script>

<style>
</style>
