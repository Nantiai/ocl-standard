export type OCLScope = {
  odoo_version?: string;
  edition?: "community" | "enterprise";
  modules?: string[];
};

export class OCLClient {
  private readonly baseUrl: string;

  constructor(baseUrl = "http://127.0.0.1:8765", private readonly accessToken?: string) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  private async call<T>(tool: string, input: Record<string, unknown>): Promise<T> {
    const response = await fetch(`${this.baseUrl}/v1/${tool.replaceAll("_", "-")}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(this.accessToken ? { authorization: `Bearer ${this.accessToken}` } : {}),
      },
      body: JSON.stringify(input),
    });
    const payload = await response.json() as {
      result?: T;
      error?: string | { code?: string; message?: string };
    };
    const error = typeof payload.error === "string" ? payload.error : payload.error?.message;
    if (!response.ok || payload.error) throw new Error(error ?? `OCL HTTP ${response.status}`);
    return payload.result as T;
  }

  getContext(question: string, options: OCLScope & Record<string, unknown> = {}) {
    return this.call("get_context", { question, ...options });
  }

  resolveNoun(noun: string, scope: OCLScope = {}) {
    return this.call("resolve_noun", { noun, ...scope });
  }

  explainField(model: string, field: string, scope: OCLScope = {}) {
    return this.call("explain_field", { model, field, ...scope });
  }

  getJoinPath(from_model: string, to_model: string, scope: OCLScope = {}) {
    return this.call("get_join_path", { from_model, to_model, ...scope });
  }

  validateWriteIntent(model: string, operation: string, options: OCLScope & Record<string, unknown> = {}) {
    return this.call("validate_write_intent", { model, operation, ...options });
  }
}
