package com.push.impl;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.misec.apiquery.ApiList;
import com.push.AbstractPush;
import com.push.model.PushMetaInfo;
import lombok.Getter;

/**
 * Push Plus 推送.
 *
 * @author itning
 * @since 2021/3/28 15:49
 */
public class PushPlusPush extends AbstractPush {

    /**
     * Push ++ 默认TOKEN长度.
     */
    public static final int PUSH_PLUS_CHANNEL_TOKEN_DEFAULT_LENGTH = 32;

    @Override
    protected String generatePushUrl(PushMetaInfo metaInfo) {
        return ApiList.PUSH_PLUS;
    }

    @Override
    protected boolean checkPushStatus(JsonObject jsonObject) {
        if (null == jsonObject) {
            return false;
        }
        // See https://www.pushplus.plus/doc/guide/api.htm
        JsonElement code = jsonObject.get("code");

        if (code == null) {
            return false;
        }

        return code.getAsInt() == 200;
    }

    @Override
    protected String generatePushBody(PushMetaInfo metaInfo, String content) {
        return new Gson().toJson(new PushModel(metaInfo.getToken(), content));
    }

    @Getter
    static class PushModel {
        private final String title = "Oldwu-HELPER任务简报";
        private final String template = "txt";
        private final String token;
        private final String content;

        public PushModel(String token, String content) {
            this.token = token;
            this.content = content;
        }
    }
}
