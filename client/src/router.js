import Vue from "vue";
import Router from "vue-router";
import Home from "./views/HomePage.vue";
import About from "./views/AboutPage.vue";
import AHJSearchPage from "./views/AHJSearchPage.vue";
import AHJHistoryPage from "./views/AHJHistoryPage.vue";
import ProductPage from "./views/ProductPage.vue";
import EditPage from "./views/EditPage.vue";
import AdminCreateProducts from "./views/AdminCreateProducts.vue";
import AdminEditProducts from "./views/AdminEditProducts.vue";
import AdminEditProduct from "./views/AdminEditProduct.vue";
import Login from "./views/Login";
import FileSubmission from "./views/FileSubmission.vue";

Vue.use(Router);

export default new Router({
  routes: [
    // {
    //   path: "/",
    //   name: "home",
    //   component: Home
    // },
    { path: "/", redirect: "/ahj-search" },
    {
      path: "/login",
      name: "login",
      component: Login
    },
    // {
    //   path: "/about",
    //   name: "about",
    //   component: About
    // },
    {
      path: "/ahj-search",
      name: "ahj-search",
      component: AHJSearchPage
    },
    {
      path: "/history",
      name: "history",
      component: AHJHistoryPage
    },
    // {
    //   path: "/product-page/:id",
    //   name: "product-page",
    //   component: ProductPage
    // },
    {
      path: "/edit",
      name: "edit",
      component: EditPage
    },
    // {
    //   path: "/admin/create-products",
    //   name: "create-products",
    //   component: AdminCreateProducts
    // },
    // {
    //   path: "/admin/edit-products",
    //   name: "edit-products",
    //   component: AdminEditProducts
    // },
    // {
    //   path: "/admin/edit-products/:id",
    //   name: "edit-product",
    //   component: AdminEditProduct
    // },
    // {
    //   path: "/submission",
    //   name: "submission",
    //   component: FileSubmission
    // }
    // {
    //   path: "/manufacturer-search",
    //   name: "manufacturer-search",
    //   component: ManufacturerSearchPage
    // }
  ]
});
