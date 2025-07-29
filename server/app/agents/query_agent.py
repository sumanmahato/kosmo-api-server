from mlx_lm import load, generate

def get_llm():
    model, tokenizer = load('/Users/samar/personal/kosmo-api-server/server/training_files/qwen_finetuned_final', tokenizer_config={"eos_token": "<|im_end|>"})
    return (model, tokenizer)

