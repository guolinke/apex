import torch
import fast_self_multihead_attn_norm_add


class FastSelfAttnNormAddFunc(torch.autograd.Function):
    @staticmethod
    def forward(ctx, use_time_mask, is_training, heads, inputs, lyr_nrm_gamma_weights, lyr_nrm_beta_weights, input_weights, output_weights, pad_mask, dropout_prob):
        heads_t        = torch.tensor([heads])
        dropout_prob_t = torch.tensor([dropout_prob])
        null_tensor    = torch.tensor([])
        use_mask       = (pad_mask is not None)
        print("---use_mask-----",use_mask)
        lyr_nrm_results,                                                \
        lyr_nrm_mean,                                                   \
        lyr_nrm_invvar,                                                 \
        input_lin_results,                                              \
        softmax_results,                                                \
        dropout_results,                                                \
        dropout_mask,                                                   \
        matmul2_results,                                                \
        dropout_add_mask,                                               \
        outputs =                                                       \
             fast_self_multihead_attn_norm_add.forward(                 \
                              use_mask,                                 \
                              use_time_mask,                            \
                              is_training,                              \
                              heads,                                    \
                              inputs,                                   \
                              lyr_nrm_gamma_weights,                    \
                              lyr_nrm_beta_weights,                     \
                              input_weights,                            \
                              output_weights,                           \
                              pad_mask if use_mask else null_tensor,    \
                              dropout_prob)

        ctx.save_for_backward(heads_t,                                  \
                              matmul2_results,                          \
                              dropout_results,                          \
                              softmax_results,                          \
                              input_lin_results,                        \
                              lyr_nrm_results,                          \
                              lyr_nrm_mean,                             \
                              lyr_nrm_invvar,                           \
                              inputs,                                   \
                              lyr_nrm_gamma_weights,                    \
                              lyr_nrm_beta_weights,                     \
                              input_weights,                            \
                              output_weights,                           \
                              dropout_mask,                             \
                              dropout_add_mask,                         \
                              dropout_prob_t)

        return outputs.detach()

    @staticmethod
    def backward(ctx, output_grads):
        heads_t,                                                        \
        matmul2_results,                                                \
        dropout_results,                                                \
        softmax_results,                                                \
        input_lin_results,                                              \
        lyr_nrm_results,                                                \
        lyr_nrm_mean,                                                   \
        lyr_nrm_invvar,                                                 \
        inputs,                                                         \
        lyr_nrm_gamma_weights,                                          \
        lyr_nrm_beta_weights,                                           \
        input_weights,                                                  \
        output_weights,                                                 \
        dropout_mask,                                                   \
        dropout_add_mask,                                               \
        dropout_prob_t          = ctx.saved_tensors

        input_grads,                                                    \
        lyr_nrm_gamma_grads,                                            \
        lyr_nrm_beta_grads,                                             \
        input_weight_grads,                                             \
        output_weight_grads    =                                        \
            fast_self_multihead_attn_norm_add.backward(                 \
                              heads_t[0],                               \
                              output_grads,                             \
                              matmul2_results,                          \
                              dropout_results,                          \
                              softmax_results,                          \
                              input_lin_results,                        \
                              lyr_nrm_results,                          \
                              lyr_nrm_mean,                             \
                              lyr_nrm_invvar,                           \
                              inputs,                                   \
                              lyr_nrm_gamma_weights,                    \
                              lyr_nrm_beta_weights,                     \
                              input_weights,                            \
                              output_weights,                           \
                              dropout_mask,                             \
                              dropout_add_mask,                         \
                              dropout_prob_t[0])

        return None, None, None,                                        \
               input_grads,                                             \
               lyr_nrm_gamma_grads,                                     \
               lyr_nrm_beta_grads,                                      \
               input_weight_grads,                                      \
               output_weight_grads,                                     \
               None, None

fast_self_attn_norm_add_func = FastSelfAttnNormAddFunc.apply
