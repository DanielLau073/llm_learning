import warnings
from langchain.chat_models import ChatOpenAI 
from langchain.prompts import ChatPromptTemplate  
from langchain.chains import LLMChain 

class LLMChainRunner:
    """
    A class for running LLMChain with a given product name prompt.

    Attributes:
    -----------
    temperature : float
        The temperature parameter for the ChatOpenAI model.
    """

    def __init__(self, temperature=0.0):
        """
        Initializes the LLMChainRunner with a given temperature parameter.

        Parameters:
        -----------
        temperature : float, optional
            The temperature parameter for the ChatOpenAI model. Default is 0.0.
        """
        self.temperature = temperature

    def run_llm_chain(self, product):
        """
        Runs LLMChain with a given product name prompt.

        Parameters:
        -----------
        product : str
            The name of the product to use as a prompt.

        Returns:
        --------
        str
            The generated company name.
        """
        warnings.filterwarnings('ignore')
        llm = ChatOpenAI(temperature=self.temperature)  
        prompt = ChatPromptTemplate.from_template("描述制造{product}的一个公司的最佳名称是什么?")
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(product)



