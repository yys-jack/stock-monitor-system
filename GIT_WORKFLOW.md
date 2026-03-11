## Git 工作流程

### 分支策略
- `master`: 主分支，用于生产环境，只接受通过测试的功能合并
- `dev`: 开发分支，日常开发工作在此分支进行

### 开发流程

1. **确认当前分支**
   - 开发前确保在 `dev` 分支：`git checkout dev`

2. **代码修改**
   - 所有代码修改必须在 `dev` 分支进行
   - 涉及修改的代码需先使用 Git 进行版本控制

3. **功能测试**
   - 修改完成后，运行相关功能进行测试
   - 确认测试成功后方可提交

4. **提交代码到 dev 分支**
   ```bash
   git add <modified_files>
   git commit -m "<type>: <description>"
   git push origin dev
   ```

   **Commit 信息格式：**
   - `feat`: 新功能
   - `fix`: Bug 修复
   - `docs`: 文档更新
   - `refactor`: 代码重构
   - `chore`: 配置/工具更新

5. **创建 Issue 并合并至 master**
   - 在 GitHub 上创建 Issue 描述变更内容
   - 创建 Pull Request 从 `dev` 合并到 `master`
   - 等待代码审查通过后合并