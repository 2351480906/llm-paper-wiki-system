## 📋 元数据 (Metadata)  
- **文献题目**：Attention Residuals  
- **文献作者**：Kimi Team  
- **发表时间**：16 March 2026  
- **发表地址/期刊会议**：arXiv preprint (cs.CL), arXiv:2603.15031v1  
- **开源代码地址**：https://github.com/MoonshotAI/Attention-Residuals  

## 📖 核心摘要 (Summary)  
本文针对现代大语言模型（LLMs）中长期沿用的固定权重残差连接（standard residual connections）提出根本性反思与改进。作者指出，尽管PreNorm+残差结构被广泛视为稳定深层训练的“梯度高速路”，但其隐含的深度方向信息聚合机制——即对所有前序层输出进行等权相加（$h_l = h_{l-1} + f_{l-1}(h_{l-1})$）——导致隐藏状态幅值随层数$L$线性增长（$O(L)$），引发严重的“PreNorm稀释效应”：早期层表征被逐步淹没，各层贡献失衡，梯度分布不均，且实证显示大量中间层可被剪枝而不显著损性能，暴露了固定聚合的结构性低效。为此，论文提出**Attention Residuals（AttnRes）**：以可学习的、输入依赖的softmax注意力机制替代固定加法，使每一层能动态选择性地聚合此前所有层的输出表示，实现内容驱动的深度维度信息路由。为缓解全层注意力带来的$O(Ld)$内存与通信开销（$L$为层数，$d$为隐藏维），作者进一步设计**Block AttnRes**——将网络划分为块，仅在块级表征间执行注意力，将复杂度降至$O(Nd)$（$N$为块数），并辅以缓存式流水线通信与双阶段计算策略，确保工程可行性。在48B参数（3B激活）的Kimi Linear架构上基于1.4T token预训练验证表明，AttnRes显著缓解PreNorm稀释，使各层输出幅值与梯度分布更均匀，并在全部下游任务中取得一致提升；缩放律实验与消融研究证实其增益具有模型规模鲁棒性及内容依赖选择机制的关键性。该工作不仅提供了残差连接的范式升级路径，更将“深度维度建模”类比于“序列维度建模”，为LLM架构设计开辟了新的理论视角与实践范式。

## 🔍 特征提取项

### 算法结构  
AttnRes的核心算法结构是对标准残差连接的深度聚合范式进行注意力化重构。在标准结构中，第$l$层输出为$h_l = h_{l-1} + f_{l-1}(h_{l-1})$，递归展开后等价于对所有前序层变换输出$\{f_0, f_1, ..., f_{l-1}\}$进行单位权重累加。AttnRes将其替换为：  
$$h_l = \sum_{i=0}^{l-1} \alpha_i^{(l)} \cdot f_i(h_i),\quad \text{where } \alpha_i^{(l)} = \mathrm{softmax}_i(\mathbf{q}^{(l)} \mathbf{k}_i^\top)$$  
其中$\mathbf{q}^{(l)}$为当前层查询向量（由$h_{l-1}$经线性投影生成），$\mathbf{k}_i$为第$i$层输出$f_i(h_i)$的键向量（经独立投影），$\alpha_i^{(l)}$为输入依赖的、可学习的深度注意力权重。为降低计算负担，Block AttnRes将$L$层划分为$N$个连续块（如每块4–8层），先在块内使用标准残差聚合得到块表征$b_j$，再对块表征集合$\{b_0, ..., b_{j-1}\}$执行注意力聚合：$h_l = \sum_{j'=0}^{j-1} \beta_{j'}^{(l)} \cdot b_{j'}$。图1(c)直观展示了其层级结构：Embedding → [Block 0: Attention+MoE] → [Block 1: Attention+MoE] → … → AttnRes Op（跨块注意力）→ Output。该结构完全兼容现有Transformer组件（如MoE、PreNorm），可作为“drop-in replacement”无缝集成。

### 训练数据集  
论文明确报告了在**1.4万亿（1.4T）tokens**的混合语料上进行了完整预训练验证。该数据集用于AttnRes在Kimi Linear架构（48B总参/3B激活）上的端到端预训练。虽然正文未详述语料构成细节（如语言比例、领域分布、去重策略），但结合Kimi团队公开技术背景，可合理推断其包含大规模中英文高质量网页、代码、学术文本及多轮对话数据，符合主流百亿至千亿级模型的典型预训练数据规模与多样性要求。此外，缩放律实验与消融分析所依赖的数据集虽未命名，但应覆盖标准LLM评估基准（如LM Evaluation Harness涵盖的多项任务），用于验证下游泛化能力。

### 训练结果表现  
AttnRes在多个维度展现出显著且一致的性能提升：（1）**内部表征健康度**：有效缓解PreNorm稀释现象，使各层输出隐藏状态的L2范数分布更均匀（而非随深度单调递增），同时梯度幅值在深度方向上呈现更平滑、更稳定的分布；（2）**下游任务性能**：在全部评估任务中均取得提升，虽未列出具体指标数值，但强调“improves downstream performance across all evaluated tasks”，表明增益具有任务普适性；（3）**可扩展性验证**：缩放律（scaling law）实验确认，AttnRes带来的性能增益在不同模型规模下保持一致，证明其非偶然性与架构级有效性；（4）**工程实用性**：Block AttnRes在保留Full AttnRes绝大部分收益的同时，将内存占用从$O(Ld)$降至$O(Nd)$（$N \ll L$），结合缓存式流水线通信与两阶段计算，实现了“minimal overhead”的工业级部署可行性。

### 创新点  
1. **范式迁移创新**：首次将注意力机制系统性引入**深度维度（depth-wise）信息聚合**，打破残差连接长达十年的固定加法范式，建立“深度即序列”的新类比框架，填补了LLM中序列维度（token-level）与深度维度（layer-level）建模不对称性的关键空白。  
2. **结构解耦创新**：提出Block AttnRes分层抽象机制，在保留注意力选择性优势的同时，通过“块内标准残差+块间注意力”的解耦设计，巧妙规避全层注意力的$O(L^2)$计算与$O(Ld)$内存瓶颈，实现理论性能与工程落地的平衡。  
3. **训练动力学优化创新**：直接针对PreNorm架构下隐藏状态幅值线性增长（$O(L)$）与梯度稀释这一深层训练不稳定根源，提供可学习的、输入自适应的调控机制，从架构层面改善梯度流与表征演化轨迹，超越传统缩放系数或归一化技巧的局部修补。  
4. **接口级兼容性创新**：设计为完全“drop-in replacement”，无需修改Attention、FFN、MoE等核心模块，仅需替换残差连接逻辑，极大降低在现有大规模训练框架（如DeepSpeed、Megatron-LM）中的集成门槛。

### 局限性  
1. **块划分策略未充分探索**：Block AttnRes的性能依赖于块大小（block size）与划分方式（如是否允许跨块跳跃、块内是否共享注意力），但论文未系统分析不同划分策略（如按功能分组vs.均匀分组）的影响，也未提出自适应块划分机制。  
2. **长程深度依赖建模受限**：即使在Full AttnRes中，因计算约束通常仅关注最近$K$层（如$K=32$），可能削弱对极深层（如>100层）全局模式的捕捉能力；Block AttnRes进一步引入块级抽象，可能损失块内细粒度的层间交互信号。  
3. **理论收敛性与泛化界缺失**：目前仅提供经验性验证（缩放律、消融），缺乏对AttnRes在优化动态、损失曲面平滑性或泛化误差上界等方面的理论分析，限制了对其鲁棒性与极限性能的深层理解。  
4. **硬件适配深度不足**：虽提及缓存式流水线通信，但未披露在特定硬件（如NVLink带宽受限的多卡集群）下的通信效率实测数据，亦未讨论其对Tensor Parallelism或Sequence Parallelism等分布式策略的潜在影响。

#

## 📚 参考文献 (References)

[1] Jacob Austin et al. Program Synthesis with Large Language Models. 2021. arXiv: 2108.07732 [cs.PL]. URL: https://arxiv.org/abs/2108.07732.

[2] Thomas Bachlechner et al. ReZero is All You Need: Fast Convergence at Large Depth. 2020. arXiv: 2003.04887 [cs.LG]. URL: https://arxiv.org/abs/2003.04887.

[3] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. Neural Machine Translation by Jointly Learning to Align and Translate. 2016. arXiv: 1409.0473 [cs.CL]. URL: https://arxiv.org/abs/1409.0473.

[4] Chen Chen and Lai Wei. Post-LayerNorm Is Back: Stable, ExpressivE, and Deep. 2026. arXiv: 2601.19895 [cs.LG]. URL: https://arxiv.org/abs/2601.19895.

[5] Mark Chen et al. Evaluating Large Language Models Trained on Code. 2021. arXiv: 2107.03374 [cs.LG]. URL: https://arxiv.org/abs/2107.03374.

[6] Peter Clark et al. “Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge”. In: arXiv:1803.05457v1 (2018).

[7] Karl Cobbe et al. Training Verifiers to Solve Math Word Problems. 2021. arXiv: 2110.14168 [cs.LG]. URL: https://arxiv.org/abs/2110.14168.

[8] Tri Dao and Albert Gu. “Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality”. In: CoRR abs/2405.21060 (2024). DOI: 10.48550/ARXIV.2405.21060. arXiv: 2405.21060. URL: https://doi.org/10.48550/arXiv.2405.21060.

[9] DeepSeek-AI et al. DeepSeek-V3 Technical Report. 2025. arXiv: 2412.19437 [cs.CL]. URL: https://arxiv. org/abs/2412.19437.

[10] Yanwen Fang et al. Cross-Layer Retrospective Retrieving via Layer Attention. 2023. arXiv: 2302.03985 [cs.CV]. URL: https://arxiv.org/abs/2302.03985.

[11] Andrey Gromov et al. The Unreasonable Ineffectiveness of the Deeper Layers. 2025. arXiv: 2403.17887 [cs.CL]. URL: https://arxiv.org/abs/2403.17887.

[12] Kaiming He et al. Deep Residual Learning for Image Recognition. 2015. arXiv: 1512.03385 [cs.CV]. URL: https://arxiv.org/abs/1512.03385.

[13] Dan Hendrycks et al. Measuring Massive Multitask Language Understanding. 2021. arXiv: 2009.03300 [cs.CY]. URL: https://arxiv.org/abs/2009.03300.

[14] Dan Hendrycks et al. Measuring Mathematical Problem Solving With the MATH Dataset. 2021. arXiv: 2103. 03874 [cs.LG]. URL: https://arxiv.org/abs/2103.03874.

[15] Jordan Hoffmann et al. Training Compute-Optimal Large Language Models. 2022. arXiv: 2203.15556 [cs.CL]. URL: https://arxiv.org/abs/2203.15556.

[16] Shengding Hu et al. MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies. 2024. arXiv: 2404.06395 [cs.CL]. URL: https://arxiv.org/abs/2404.06395.

[17] Gao Huang et al. Densely Connected Convolutional Networks. 2018. arXiv: 1608.06993 [cs.CV]. URL: https://arxiv.org/abs/1608.06993.

[18] Yanping Huang et al. “GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism”. In: Advances in NeurIPS. 2019.

[19] Yuzhen Huang et al. “C-eval: A multi-level multi-discipline chinese evaluation suite for foundation models”. In: Advances in NeurIPS 36 (2023), pp. 62991–63010.

[20] Robert A. Jacobs et al. “Adaptive Mixtures of Local Experts”. In: Neural Computation 3.1 (1991), pp. 79–87. DOI: 10.1162/neco.1991.3.1.79.

[21] Mandar Joshi et al. “Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension”. In: arXiv preprint arXiv:1705.03551 (2017).

[22] Jared Kaplan et al. Scaling Laws for Neural Language Models. 2020. arXiv: 2001.08361 [cs.LG]. URL: https://arxiv.org/abs/2001.08361.

[23] Angelos Katharopoulos et al. “Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention”. In: Proceedings of ICML. Ed. by Hal Daumé III and Aarti Singh. PMLR, 2020, pp. 5156–5165. URL: https: //proceedings.mlr.press/v119/katharopoulos20a.html.

[24] Jonas Knupp et al. Depth-Recurrent Attention Mixtures: Giving Latent Reasoning the Attention it Deserves. 2026. arXiv: 2601.21582 [cs.AI]. URL: https://arxiv.org/abs/2601.21582.

[25] Aitor Lewkowycz et al. Solving Quantitative Reasoning Problems with Language Models. 2022. arXiv: 2206. 14858 [cs.CL]. URL: https://arxiv.org/abs/2206.14858. 17 Attention Residuals TECHNICAL REPORT

[26] Haonan Li et al. “CMMLU: Measuring massive multitask language understanding in Chinese”. In: Findings of the Association for Computational Linguistics: ACL 2024. Ed. by Lun-Wei Ku, Andre Martins, and Vivek Srikumar. Bangkok, Thailand: Association for Computational Linguistics, Aug. 2024, pp. 11260–11285. DOI: 10 . 18653 / v1 / 2024 . findings - acl .

671. URL: https : / / aclanthology . org / 2024 . findings acl.671/.

[27] Tianyu Li et al. SiameseNorm: Breaking the Barrier to Reconciling Pre/Post-Norm. 2026. arXiv: 2602.08064 [cs.LG]. URL: https://arxiv.org/abs/2602.08064.

[28] Jingyuan Liu et al. Muon is Scalable for LLM Training. 2025. arXiv: 2502.16982 [cs.LG]. URL: https: //arxiv.org/abs/2502.16982.

[29] Brian Mak and Jeffrey Flanigan. Residual Matrix Transformers: Scaling the Size of the Residual Stream. 2025. arXiv: 2506.22696 [cs.LG]. URL: https://arxiv.org/abs/2506.22696.

[30] Gaurav Menghani, Ravi Kumar, and Sanjiv Kumar. LAuReL: Learned Augmented Residual Layer. 2025. arXiv: 2411.07501 [cs.LG]. URL: https://arxiv.org/abs/2411.07501.

[31] Maxim Milakov and Natalia Gimelshein. Online normalizer calculation for softmax. 2018. arXiv: 1805.02867 [cs.PF]. URL: https://arxiv.org/abs/1805.02867.

[32] Tsendsuren Munkhdalai et al. “Metalearned Neural Memory”. In: ArXiv abs/1907.09720 (2019). URL: https: //api.semanticscholar.org/CorpusID:198179407.

[33] Deepak Narayanan et al. Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM. 2021. arXiv: 2104.04473 [cs.CL]. URL: https://arxiv.org/abs/2104.04473.

[34] Toan Q. Nguyen and Julian Salazar. “Transformers without Tears: Improving the Normalization of SelfAttention”. In: Proceedings of IWSLT. Ed. by Jan Niehues et al. 2019. URL: https : / / aclanthology . org/2019.iwslt-1.17/.

[35] OpenAI et al. GPT-4 Technical Report. 2024. arXiv: 2303.08774 [cs.CL]. URL: https://arxiv.org/abs/ 2303.08774.

[36] Matteo Pagliardini et al. DenseFormer: Enhancing Information Flow in Transformers via Depth Weighted Averaging. 2024. arXiv: 2402.02622 [cs.CL]. URL: https://arxiv.org/abs/2402.02622.

[37] Bowen Peng et al. “Yarn: Efficient context window extension of large language models”. In: arXiv preprint arXiv:2309.00071 (2023).

[38] Matthew E. Peters et al. “Deep Contextualized Word Representations”. In: Proceedings of NAACL. 2018, pp. 2227–2237. URL: https://aclanthology.org/N18-1202/.

[39] Reiner Pope et al. Efficiently Scaling Transformer Inference. 2022. arXiv: 2211.05102 [cs.LG].

[40] Zhen Qin et al. HGRN2: Gated Linear RNNs with State Expansion. 2024. arXiv: 2404.07904 [cs.CL].

[41] David Rein et al. “Gpqa: A graduate-level google-proof q&a benchmark”. In: First Conference on Language Modeling. 2024.

[42] Imanol Schlag, Kazuki Irie, and Jürgen Schmidhuber. “Linear Transformers Are Secretly Fast Weight Programmers”. In: Proceedings of ICML. Ed. by Marina Meila and Tong Zhang. PMLR, 2021, pp. 9355–9366. URL: https://proceedings.mlr.press/v139/schlag21a.html.

[43] Jürgen Schmidhuber. “Learning to control fast-weight memories: An alternative to dynamic recurrent networks”. In: Neural Computation 4.1 (1992), pp. 131–139.

[44] Freda Shi et al. Language Models are Multilingual Chain-of-Thought Reasoners. 2022. arXiv: 2210.03057 [cs.CL]. URL: https://arxiv.org/abs/2210.03057.

[45] Rupesh Kumar Srivastava, Klaus Greff, and Jürgen Schmidhuber. Highway Networks. 2015. arXiv: 1505.00387 [cs.LG]. URL: https://arxiv.org/abs/1505.00387.

[46] Yu Sun et al. “Learning to (Learn at Test Time): RNNs with Expressive Hidden States”. In: ArXiv abs/2407.04620 (2024). URL: https://api.semanticscholar.org/CorpusID:271039606.

[47] Yutao Sun et al. Retentive Network: A Successor to Transformer for Large Language Models. 2023. arXiv: 2307.08621 [cs.CL].

[48] Mirac Suzgun et al. “Challenging big-bench tasks and whether chain-of-thought can solve them”. In: arXiv preprint arXiv:2210.09261 (2022).

[49] Shawn Tan et al. “Scaling Stick-Breaking Attention: An Efficient Implementation and In-depth Study”. In: Proceedings of ICLR. 2025.

[50] Hugo Touvron et al. Going deeper with Image Transformers. 2021. arXiv: 2103.17239 [cs.CV]. URL: https: //arxiv.org/abs/2103.17239.

[51] Hugo Touvron et al. LLaMA: Open and Efficient Foundation Language Models. 2023. arXiv: 2302.13971 [cs.CL]. 18 Attention Residuals TECHNICAL REPORT

[52] Ashish Vaswani et al. “Attention is All you Need”. In: Advances in NeurIPS. Ed. by I. Guyon et al. Curran Associates, Inc., 2017. URL: https://proceedings.neurips.cc/paper_files/paper/2017/file/ 3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf.

[53] Ashish Vaswani et al. “Attention is All you Need”. In: Advances in NeurIPS. Ed. by I. Guyon et al. Vol.

30. Curran Associates, Inc., 2017. URL: https://proceedings.neurips.cc/paper_files/paper/2017/ file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf.

[54] Hongyu Wang et al. DeepNet: Scaling Transformers to 1,000 Layers. 2022. arXiv: 2203.00555 [cs.CL]. URL: https://arxiv.org/abs/2203.00555.

[55] Yubo Wang et al. “Mmlu-pro: A more robust and challenging multi-task language understanding benchmark”. In: Advances in NeurIPS 37 (2024), pp. 95266–95290.

[56] Da Xiao et al. “MUDDFormer: Breaking Residual Bottlenecks in Transformers via Multiway Dynamic Dense Connections”. In: Proceedings of ICML. 2025.

[57] Guangxuan Xiao et al. “Efficient streaming language models with attention sinks”. In: arXiv preprint arXiv:2309.17453 (2023).

[58] Tian Xie. Your DeepSeek mHC Might Not Need the “m”. Zhihu blog post. 2026. URL: https://zhuanlan. zhihu.com/p/2010852389670908320.

[59] Zhenda Xie et al. mHC: Manifold-Constrained Hyper-Connections. 2026. arXiv: 2512.24880 [cs.CL]. URL: https://arxiv.org/abs/2512.24880.

[60] Ruibin Xiong et al. On Layer Normalization in the Transformer Architecture. 2020. arXiv: 2002.04745 [cs.LG]. URL: https://arxiv.org/abs/2002.04745.

[61] Bowen Yang et al. Rope to Nope and Back Again: A New Hybrid Attention Strategy. 2025. arXiv: 2501.18795 [cs.CL]. URL: https://arxiv.org/abs/2501.18795.

[62] Songlin Yang, Jan Kautz, and Ali Hatamizadeh. “Gated Delta Networks: Improving Mamba2 with Delta Rule”. In: Proceedings of ICLR. 2025. URL: https://openreview.net/forum?id=r8H7xhYPwz.

[63] Songlin Yang et al. “Gated Linear Attention Transformers with Hardware-Efficient Training”. In: Proceedings of ICML. PMLR, 2024.

[64] Yongyi Yang and Jianyang Gao. mHC-lite: You Don’t Need 20 Sinkhorn-Knopp Iterations. 2026. arXiv: 2601. 05732 [cs.LG]. URL: https://arxiv.org/abs/2601.05732.

[65] Rowan Zellers et al. “HellaSwag: Can a Machine Really Finish Your Sentence?” In: Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics. 2019.

[66] Biao Zhang and Rico Sennrich. “Root mean square layer normalization”. In: Advances in NeurIPS 32 (2019).

[67] Yifan Zhang et al. Deep Delta Learning. 2026. arXiv: 2601.00417 [cs.LG]. URL: https://arxiv.org/ abs/2601.00417.

[68] Yilang Zhang et al. ANCRe: Adaptive Neural Connection Reassignment for Efficient Depth Scaling. 2026. arXiv: 2602.09009 [cs.LG]. URL: https://arxiv.org/abs/2602.09009.

[69] Yu Zhang et al. Kimi Linear: An Expressive, Efficient Attention Architecture. 2025. arXiv: 2510.26692 [cs.CL].

[70] Shu Zhong et al. Understanding Transformer from the Perspective of Associative Memory. 2025. arXiv: 2505. 19488 [cs.LG]. URL: https://arxiv.org/abs/2505.19488.

[71] Zhanchao Zhou et al. “Value Residual Learning”. In: Proceedings of ACL. Ed. by Wanxiang Che et al. Vienna, Austria, 2025, pp. 28341–28356. URL: https://aclanthology.org/2025.acl-long.1375/.

[72] Defa Zhu et al. Hyper-Connections. 2025. arXiv: 2409.19606 [cs.LG]. URL: https://arxiv.org/abs/ 2409.19606.

[73] Zhijian Zhuo et al. HybridNorm: Towards Stable and Efficient Transformer Training via Hybrid Normalization. 2025. arXiv: 2503.04598 [cs.CL]. URL: https://arxiv.org/abs/2503.04598. 19 Attention Residuals TECHNICAL REPORT A Contributions The authors are listed in order of the significance of their contributions, with those in project leadership roles appearing last. Guangyu Chen∗ Yu Zhang∗ Jianlin Su∗ Weixin Xu Siyuan Pan Yaoyu Wang Yucheng Wang Guanduo Chen Bohong Yin Yutian Chen Junjie Yan Ming Wei Y. Zhang Fanqing Meng Chao Hong Xiaotong Xie Shaowei Liu Enzhe Lu Yunpeng Tai Yanru Chen Xin Men Haiqing Guo Y. Charles Haoyu Lu Lin Sui Jinguo Zhu Zaida Zhou Weiran He Weixiao Huang Xinran Xu Yuzhi Wang Guokun Lai Yulun Du Yuxin Wu Zhilin Yang Xinyu Zhou ∗Equal contribution 20 Attention Residuals TECHNICAL REPORT B Optimized Inference I/O for Full Attention Residuals A naïve implementation of Full AttnRes scans all preceding layer outputs at every layer, so memory traffic scales linearly with depth. As noted in §4.2, however, the pseudo-query wl is a learned parameter independent of both the input and the hidden state. We can therefore batch inter-block accesses across layers in a two-phase schedule, bringing total I/O well below the naïve bound. Note that the block partition introduced below is purely an inference scheduling device. Unlike Block AttnRes, it leaves the model architecture unchanged and does not replace per-layer sources with block summaries; it simply makes the amortization argument concrete. Setup Let the model have L layers and hidden dimension d, partitioned into N contiguous blocks of size S = L/N. Inference proceeds one block at a time: Phase 1 jointly computes inter-block attention for all S layers in the block against all preceding blocks, and Phase 2 walks through intra-block dependencies sequentially. Phase 1: Batched Inter-block Attention Consider block n with its S layers. The queries {wl}l∈Bn are all known before execution begins, so the (n−1)S preceding key–value pairs need only be read once from HBM and reused across all S queries. The read cost for block n is therefore Read(n) inter = 2(n −1)Sd, (11) where the factor of 2 accounts for both keys and values. Summing over all N blocks and using SN = L: Readinter = N X n=1 2(n −1)Sd = 2Sd · N(N −1) 2 = dL(N −1). (12) Phase 1 also writes one d-dimensional output per layer, giving Write(n) inter = Sd per block and Writeinter = Ld (13) in total. Phase 2: Sequential Intra-block Attention Phase 1 covers all sources before the current block. Within the block, however, each layer depends on those before it, so these must be handled in order. Layer t (1 ≤t ≤S) reads t−1 intra-block key–value pairs at a cost of 2(t−1)d. Summing over one block: Read(n) intra = S X t=1 2(t −1)d = S(S −1)d. (14) Phase 2 also writes one output per layer, so Write(n) intra = Sd. Total Amortized I/O per Layer Summing both phases over all N blocks: Readtotal = dL(N −1) + N · S(S −1)d, Writetotal = 2Ld. (15) Dividing by L and using SN = L: Read per layer = (N −1)d + (S −1)d = (S + N −2)d, Write per layer = 2d, (16) Total I/O per layer = (S + N) d. (17) Batching inter-block reads thus brings per-layer I/O from O(L) down to O(S+N). The schedule follows the same two-phase split as Block AttnRes: inter-block attention accounts for the bulk of the traffic, while sequential computation stays local within each block. 21