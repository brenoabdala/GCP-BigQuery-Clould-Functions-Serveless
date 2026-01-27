<h1>GCP BigQuery Cloud Functions Serverless</h1>

<p>
Pipeline automatizado de ingestão e processamento de dados utilizando arquitetura 100% Serverless no Google Cloud Platform.
</p>

<hr>

<h2>Sobre o Projeto</h2>

<p>
Este projeto demonstra a implementação de um fluxo de Engenharia de Dados moderno. Ele utiliza Cloud Functions (2ª Geração) para processar dados via Python e Pandas, realizando a carga automatizada no BigQuery.
</p>

<hr>

<h2>Guia de Implementação (Passo a Passo)</h2>

<h3>1. Criar e Configurar a Function via VS Code</h3>

<p>Para desenvolver localmente e manter o código organizado:</p>

<ol>
  <li>
    <b>Estrutura de Arquivos:</b>
    Crie uma pasta e adicione os arquivos main.py (lógica) e requirements.txt (dependências).
  </li>

  <li>
    <b>Autenticação:</b>
    Abra o terminal do VS Code e logue na sua conta Google:
  </li>
</ol>

<pre><code>gcloud auth login</code></pre>

<p>
<b>Seleção de Projeto:</b>
Defina o projeto onde a função será hospedada:
</p>

<pre><code>gcloud config set project SEU_ID_DO_PROJETO</code></pre>

<hr>

<h3>2. Realizar o Deploy</h3>

<p>
O comando abaixo realiza o upload do código e configura o ambiente de execução:
</p>

<pre><code>gcloud functions deploy funcao-vendas-app \
--gen2 \
--runtime=python310 \
--region=southamerica-east1 \
--source=. \
--entry-point=hello_get \
--trigger-http \
--allow-unauthenticated
</code></pre>

<p>
<b>Nota:</b> Se o PowerShell bloquear a execução, use o comando:
</p>

<pre><code>Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser</code></pre>

<hr>

<h3>3. Configurar o Cloud Scheduler (Gatilho Diário)</h3>

<p>
Para rodar a função automaticamente (ex: às 10h da manhã):
</p>

<ol>
  <li>Acesse o Cloud Scheduler no Console do GCP.</li>
  <li>Clique em Criar Job e defina:</li>
</ol>

<p><b>Frequência:</b></p>

<pre><code>0 10 * * *</code></pre>

<p>(Cron para 10h AM)</p>

<p>
<b>Fuso Horário:</b> Brasil/São Paulo (GMT-3)
</p>

<p><b>Na configuração do Destino:</b></p>

<ul>
  <li><b>URL:</b> Cole a URL gerada no deploy da sua Function.</li>
  <li><b>Método HTTP:</b> GET.</li>
  <li><b>Auth Header:</b> Selecione "Add OIDC token" e escolha a conta de serviço padrão.</li>
</ul>

<hr>

<h2>Arquitetura da Solução</h2>

<ul>
  <li><b>Trigger:</b> Cloud Scheduler (Cron Job).</li>
  <li><b>Compute:</b> Cloud Function Python (Pandas ETL).</li>
  <li><b>Storage:</b> BigQuery Data Warehouse.</li>
  <li><b>Segurança:</b> Gerenciamento via IAM Service Accounts.</li>
</ul>

<hr>

<h2>Tecnologias e Bibliotecas</h2>

<ul>
  <li>google-cloud-bigquery</li>
  <li>pandas</li>
  <li>functions-framework</li>
  <li>pyarrow</li>
</ul>
