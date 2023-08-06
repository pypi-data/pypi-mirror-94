# jkPyUtils

Common Utils for Python from Jackon

[https://pypi.org/project/jkPyUtils](https://pypi.org/project/jkPyUtils)


## API doc

TODO

- requests2: get text / binary, use cache
- cache

Try examples:

```bash
python samples/requests2/demo_requests2.py
```

## 贡献代码

#### 开发环境

```bash
make dev-setup
```

#### 测试

```bash
make test
```

#### 发布

1. Testing before release

```bash
$ make build
$ make install
```

3. Run examples:

```bash
$ python3 examples/show_placeholder.py
```

4. Release to pypi

```bash
$ make build
$ make upload
```
