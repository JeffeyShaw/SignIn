package com.netmusic.controller;

import com.netmusic.model.AutoNetmusic;
import com.netmusic.service.NetmusicService;
import com.oldwu.entity.AjaxResult;
import com.oldwu.security.utils.SessionUtils;
import com.oldwu.service.UserService;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;
import java.util.Map;

@RestController
@RequestMapping("/api/user/netmusic")
public class NetMusicController {

    @Autowired
    private NetmusicService netmusicService;

    @Autowired
    private UserService userService;

    /**
     * 根据id查询详细信息
     * @param id
     * @return
     */
    @PostMapping("/view")
    public AjaxResult view(@Param("id") Integer id) {
        return netmusicService.view(id);
    }

    /**
     * 获取这个用户的网易云托管列表
     * @return
     */
    @PostMapping("/list")
    public AjaxResult list() {
        Integer id = SessionUtils.getPrincipal().getId();
        return netmusicService.listMine(id);
    }

    @PostMapping("/edit")
    public Map<String, Object> edit(@RequestBody AutoNetmusic autoNetmusic, Principal principal) {
        autoNetmusic.setUserid(userService.getUserId(principal.getName()));
        return netmusicService.editNetMusicPlan(autoNetmusic);
    }

    @PostMapping("/delete")
    public AjaxResult delete(@Param("id") Integer id) {
        try {
            return netmusicService.deleteNetMusicPlan(id);
        } catch (Exception e) {
            return AjaxResult.doError(e.getMessage());
        }
    }

    @PostMapping("/add")
    public Map<String, String> add(@RequestBody AutoNetmusic autoNetmusic, Principal principal) {
        autoNetmusic.setUserid(userService.getUserId(principal.getName()));
        return netmusicService.addNetMusicPlan(autoNetmusic);
    }

    @PostMapping("/run")
    public Map<String, Object> run(@Param("id") Integer id, Principal principal) {
        Integer userId = userService.getUserId(principal.getName());
        return netmusicService.doDailyTaskPersonal(id,userId);
    }

}
