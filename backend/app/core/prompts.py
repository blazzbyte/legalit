class Prompts:

    _keywords = '''
    USER QUESTION:
    {instruction}
    """Based on the user question, give me one or more keywords and variation of these keywords related to legal that can help answer the user question. A few examples: Article 87, section II"""
    '''

    _keywords_with_document = '''
    DOCUMENT:
    {document}
    USER QUESTION:
    {instruction}
    INSTRUCTION:
    """Based on the document, give me one or more keywords and variation of these keywords related to legal that can help answer the user question. A few examples: Art. 87, Article 87, section 12, civil law, etc."""
    KEYWORDS:
    '''

    _analyst = '''
    # LEGAL CONTEXT:
    {context}
    """Based on the legal context. Respond the user question as better as you can:"""
    # USER QUESTION:
    {instruction}
    '''

    _analyst_with_document = '''
    LEGAL CONTEXT:
    {context}
    DOCUMENT:
    {document}
    """Based on the legal context and reviewing each part of the document. Respond the user question as better as you can:"""
    USER QUESTION:
    {instruction}
    '''

    # #### Analyze each clause and provision of the legal document, looking for possible areas of compliance or non-compliance. Provide a detailed report summarizing your findings, including any discrepancies or potential risks of non-compliance. Ensure the assessment is thorough and accurate, providing clear recommendations and corrective actions if necessary.

    @staticmethod
    def formatPromptKeywords(instruction: str, document: str = "") -> str:
        if document:
            return Prompts._keywords_with_document.format(instruction=instruction, document=document)
        else:
            return Prompts._keywords.format(instruction=instruction)

    @staticmethod
    def formatPromptAnalyst(instruction: str, context: str = "", document: str = "") -> str:
        if document:
            return Prompts._analyst_with_document.format(context=context, instruction=instruction, document=document)
        else:
            return Prompts._analyst.format(context=context, instruction=instruction)
