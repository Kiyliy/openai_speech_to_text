# openai_speech_to_text
# 语音转文字软件

这是一个使用Python编写的语音转文字应用程序，它允许用户通过OPENAI-API将语音实时转换为文字。

适配Windows, 解决Windows打字烦恼

## 特色

本软件由GPT-4提供技术支持

## 功能

- [x] 自定义API-Key
- [x] 自定义URL
- [x] 双击Ctrl控制录音
- [x] 文字自动写入光标所在文本框
- [x] 支持log显示, 方便必要时手动复制

## 下一版本

- [ ] 支持语言选择
- [ ] 优化UI页面
- [ ] 提供浏览器插件版本

## 快速开始

下载最新的[发布版本](https://github.com/Kiyliy/openai_speech_to_text/releases/)，解压并运行可执行文件即可开始使用。

注意: URL需要填写完整的请求地址:
示例: https://api.openai.com/v1/audio/transcriptions

## 开发

如果您想查看源代码或参与贡献，请克隆仓库并安装所需的依赖项：

```bash
git clone https://github.com/Kiyliy/openai_speech_to_text.git
cd openai_speech_to_text
```

## 细节介绍:

默认要求使用简体中文回复, 下个版本会支持语言选择

```
 "prompt": "Use simplified Chinese"
```



## 贡献

欢迎贡献！请提交pull requests给我们。

## 许可证

此项目遵循MIT许可证。详情请见LICENSE文件。

## 致谢

- 感谢OpenAI提供API支持
- 感谢所有测试者和贡献者的宝贵意见