<script setup>
import { ref, reactive } from 'vue';
import DataTable from 'datatables.net-vue3'

const idInput = ref("");
const nameInput = ref("");
const phoneInput = ref("");
const addressInput = ref("");
const otherInput = ref("");
const resultget = reactive([])  //只能是 陣列或字典
//身分證錯誤訊息
const msgId = ref("");
const msgIdClassEr = ref(false);
const idInputClassEr = ref(false);
//電話錯誤訊息
const msgPh = ref("");
const msgPhClassEr = ref(false);
const phoneInputClassEr = ref(false);
//表格
const dataTable = ref([])
const highlightId = ref('')
const animation = ref(false)
const deleteId = ref('')
const showTable = ref(false)

//取得輸入框內容
function getListData() {
  return {
    id: idInput.value.trim().toUpperCase(),
    name: nameInput.value.trim(),
    phone: phoneInput.value.trim(),
    address: addressInput.value.trim(),
    other: otherInput.value.trim(),
  };
}

//設定輸入框內容
function setInputVal(data) {
  idInput.value = data.id;
  nameInput.value = data.name;
  phoneInput.value = data.phone;
  addressInput.value = data.address;
  otherInput.value = data.other;
}

//處理後端後端錯誤
function handleApiFailure(result) {
  if (!result.success) {
    alert(result.message);
    return true;
  }
  return false;
}

const columns = [
  { data: 'id', title: '身分證字號' },
  { data: 'name', title: '姓名' },
  { data: 'phone', title: '電話' },
  { data: 'address', title: '地址' },
  { data: 'other', title: '備註' },
];

const options = {
  order: [],      //不排序
  language: {
    url: '/zh-HANT.json',
  },
  createdRow: function (tr, data, dataIndex) {
    if (data.id === highlightId.value) {
      tr.classList.add('highlight')
    }
    if (animation.value) {
      tr.classList.add('data')
      setTimeout(() => {
        tr.classList.add('slip')
      }, (dataIndex + 1) * 100)
    }
    if (data.id === deleteId.value) {
      tr.classList.add('dataDel')
      setTimeout(() => {
        tr.classList.add('slipOut')
      }, 50)
    }
  },
  rowCallback: function (tr, data) {
    tr.addEventListener('click', function () {
      setInputVal(data)
    })
  },
  headerCallback: function (thead) {
    thead.classList.add('table-dark')
  },
}

//處理datatable表格
function setDataTable(data, highlight, anim) {
  showTable.value = true
  dataTable.value = data
  highlightId.value = highlight
  animation.value = anim
}

//顯示身分證錯誤訊息
function showIdErro(msg) {
  msgId.value = msg;
  msgIdClassEr.value = true;
  idInputClassEr.value = true;
}

//移除身分證錯誤訊息
function clearIdErro(msg, correct = false) {
  msgId.value = msg;
  msgIdClassEr.value = false;
  idInputClassEr.value = false;
  if (correct) {
    showCorrect.value = true;
    setTimeout(() => {
      showCorrect.value = false;
    }, 1000);
  }
}

//顯示電話錯誤訊息
function showPhErro(msg) {
  msgPh.value = msg;
  msgPhClassEr.value = true;
  phoneInputClassEr.value = true;
}

//移除電話錯誤訊息
function clearPhErro(msg) {
  msgPh.value = msg;
  msgPhClassEr.value = false;
  phoneInputClassEr.value = false;
}

//身分證檢查
const showCorrect = ref(false);

function idCheck(id) {
  if (id === "") {
    clearIdErro("", false);
    return null;
  } else if (id.length < 10) {
    showIdErro("請輸入完整身分證號");
    return false;
  } else if (!checkId(id)) {
    showIdErro("身份證字號檢碼不符");
    return false;
  } else {
    clearIdErro("身份證字號檢碼正確", true);
    return true;
  }
}

//手機號檢查
function phCheck(ph) {
  if (ph === "") {
    clearPhErro("");
    return null;
  } else if (!/^\d+$/.test(ph)) {
    showPhErro("請輸入數字手機號碼");
    return false;
  }
}

//檢查全部顯示警示訊息
function Check() {
  const idResult = idCheck(idInput.value);
  const phResult = phCheck(phoneInput.value);

  if (idResult === null) {
    alert("請輸入身分證號");
    return false;
  } else if (idResult == false) {
    alert("身份證字號檢碼不符");
    return false;
  } else if (nameInput.value === "") {
    alert("請輸入姓名");
    return false;
  } else if (phResult === null) {
    alert("請輸入手機號碼");
    return false;
  } else if (phResult === false) {
    alert("請輸入數字手機號碼");
    return false;
  } else if (addressInput.value === "") {
    alert("請輸入地址");
    return false;
  }
  return true;
}

//身分證檢碼計算
function checkId(id) {
  const letter = {
    A: 10, B: 11, C: 12, D: 13, E: 14, F: 15, G: 16, H: 17,
    I: 34, J: 18, K: 19, L: 20, M: 21, N: 22, O: 35, P: 23,
    Q: 24, R: 25, S: 26, T: 27, U: 28, V: 29, W: 32, X: 30,
    Y: 31, Z: 33
  };

  if (/^[A-Z][12]\d{8}$/.test(id)) {
    const code = letter[id[0]];

    const nums = [Math.floor(code / 10), code % 10];

    for (let i = 1; i < 9; i++) {
      nums.push(parseInt(id[i]));
    }
    const weight = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1];

    let sum = 0;
    for (let i = 0; i < weight.length; i++) {
      sum += nums[i] * weight[i];
    }

    const check = sum % 10;
    let checknNm = (10 - check) % 10;
    const correct = parseInt(id[9]) === checknNm;

    return correct;
  }
}

//取得 顯示資料
async function loadList(highlightId = null, animation = false) {
  const res = await fetch("/api/users", { method: "GET" }); //後端請求資料
  const result = await res.json(); //轉 js 陣列
  resultget.push(...result.data)  //... 把原本的陣列資料一個一個重新插入 resultget 的陣列裡
  console.log('resultget :>> ', resultget);


  if (handleApiFailure(result)) {
    //處理後端錯誤
    return;
  }

  console.log(result);

  setDataTable(result.data, highlightId, animation);
}

//查詢
async function get() {
  const id = idInput.value.trim().toUpperCase();

  if (id === "") {
    alert("請輸入身分證號");
    return;
  }

  const res = await fetch(`/api/users/${id}`, { method: "GET" });
  const result = await res.json();

  if (handleApiFailure(result)) {
    //處理後端錯誤
    return;
  }

  console.log(result);

  setInputVal(result.data);

  setDataTable([result.data], null, true);
}

//新增
async function post() {
  if (!Check()) {
    return;
  }

  const data = getListData();

  const res = await fetch("/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const result = await res.json();

  if (handleApiFailure(result)) {
    //處理後端錯誤
    return;
  }

  console.log(result);
  console.log(result.data.id);

  setTimeout(() => {
    alert(result.message);
  }, 1000);

  setInputVal("");

  loadList(result.data.id);
}

//修改
async function put() {
  const data = getListData();
  const id = data.id;

  if (id === "") {
    alert("請選擇要修改的列");
    return;
  } else if (!Check()) {
    return;
  }

  const res = await fetch(`/api/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await res.json();

  if (handleApiFailure(result)) {
    //處理後端錯誤
    return;
  }
  setTimeout(() => {
    alert(result.message);
  }, 1000);

  loadList(result.data.id);
}

//刪除
async function idDelete() {
  const data = getListData();
  const id = data.id;
  console.log(id);

  if (id === "") {
    alert("請選擇要刪除的列");
    return;
  }

  const res = await fetch(`/api/users/${id}`, { method: "DELETE" });
  const result = await res.json();

  if (handleApiFailure(result)) {
    //處理後端錯誤
    return;
  }

  deleteId.value = id


  setTimeout(() => {
    deleteId.value = null
    loadList();
  }, 800);

  setTimeout(() => {
    alert(result.message);
  }, 1000);
}

</script>

<template>
  <div class="content">
    <div class="input-btn">
      <div class="input">
        <div class="input-group flex-nowrap">
          <span class="input-group-text" id="id-span">身份證字號</span>
          <input type="text" v-model="idInput" class="form-control" :class="{ 'is-invalid': idInputClassEr }"
            aria-label="Username" aria-describedby="addon-wrapping" @input="idCheck(idInput.trim().toUpperCase())">
        </div>
        <div id="msgId" class="msg" :class="{ 'show': msgIdClassEr, 'showCorrect': showCorrect }">{{ msgId }}
        </div>
        <div class="input-group flex-nowrap">
          <span class="input-group-text" id="name-span">姓名</span>
          <input type="text" v-model="nameInput" class="form-control" aria-label="name"
            aria-describedby="addon-wrapping">
        </div>
        <div class="input-group flex-nowrap">
          <span class="input-group-text" id="phone-span">電話</span>
          <input type="text" v-model="phoneInput" class="form-control" :class="{ 'is-invalid': phoneInputClassEr }"
            aria-label="phone" aria-describedby="addon-wrapping" @input="phCheck(phoneInput)">
        </div>
        <div id="msgPh" class="msgPh" :class="{ 'show': msgPhClassEr }">{{ msgPh }}</div>
        <div class="input-group flex-nowrap">
          <span class="input-group-text" id="address-span">地址</span>
          <input type="text" v-model="addressInput" class="form-control" aria-label="address"
            aria-describedby="addon-wrapping">
        </div>
        <div class="input-group flex-nowrap">
          <span class="input-group-text" id="other-span">備註</span>
          <input type="text" v-model="otherInput" class="form-control" aria-label="other"
            aria-describedby="addon-wrapping">
        </div>
      </div>
      <div class="Btns">
        <button id="getBtn" class="btn btn-outline-primary" @click="get">查詢</button>
        <button id="postBtn" class="btn btn-outline-primary" @click="post">新增</button>
        <button id="putBtn" class="btn btn-outline-primary" @click="put">修改</button>
        <button id="deleteBtn" class="btn btn-outline-primary" @click="idDelete">刪除</button>
        <button id="listBtn" class="btn btn-outline-primary" @click="loadList(null, true)">列表</button>
      </div>
    </div>
    <transition name="fade">
      <div class="Table" v-if="showTable">
        <!-- <table class="table table-striped"></table>  使用 bootstrap-->
        <!-- id="dataTable" class="table table-striped border border-secondary-subtle" -->
        <DataTable class="table table-striped border border-secondary-subtle" :columns="columns" :data="dataTable"
          :options="options" />
      </div>
    </transition>
  </div>
</template>

<style scoped>
.content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-btn {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.msg {
  opacity: 0;
  height: 0;
  font-size: 10px;
  overflow: hidden;
  padding-left: 120px;
  transition: height 0.5s ease-in-out;
}

.msg.show {
  opacity: 1;
  height: 15px;
  color: red;
}

.msg.showCorrect {
  opacity: 1;
  height: 15px;
  color: green;
}

.msgPh {
  opacity: 0;
  height: 0;
  font-size: 10px;
  overflow: hidden;
  padding-left: 60px;
  transition: height 0.5s ease-in-out;
}

.msgPh.show {
  opacity: 1;
  height: 15px;
  color: red;
}

.msgPh.showCorrect {
  opacity: 1;
  height: 15px;
  color: green;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

.Table {
  /* display: none; */
  overflow: hidden;
}

:deep(.dataTable th),
/* datatable 初始化就有綁定 class='dataTable' 不用另外寫*/
:deep(.dataTable td) {
  text-align: center;
}

:deep(.dataTable tr:hover td) {
  background-color: #cce0ff;
  transform: scale(1.05);
  font-weight: bold;
  cursor: pointer;
}

:deep(.dataTable tr:active td) {
  background-color: #99ccff
}

:deep(tr.data) {
  opacity: 0;
  transform: translateX(100%);
  transition: all 0.5s ease-in-out;
}

:deep(tr.slip) {
  opacity: 1;
  transform: translateX(0);
}

:deep(tr.dataDel) {
  opacity: 1;
  transform: translateX(0%) scale(1.1);
  transition: all 0.8s ease-in-out;
}

:deep(tr.slipOut) {
  opacity: 0;
  transform: translateX(100%) scale(-1);
}

:deep(tr.highlight td) {
  /* tr 在 html 不能做單獨動畫，只能針對 td */
  animation: add 1.5s ease-in-out;
}

@keyframes add {
  0% {
    background-color: #fff8b3;
  }

  100% {
    background-color: transparent;
  }
}
</style>
