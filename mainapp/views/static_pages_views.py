from django.http import Http404
from django.shortcuts import render


PAGE_CONTENT = {
    'about-us': {
        'title': 'About Us',
        'sections': [
            {
                'heading': 'About Us',
                'paragraphs': [
                    "At CREATE PASSION Fashion, we believe that fashion is not just about clothing; it's a statement of style, personality, and confidence. We are a leading fashion brand that caters to both men and women, offering a wide range of clothing and accessories to suit every taste and occasion.",
                    "At CREATE PASSION Fashion, we are more than just a clothing brand; we are a community of fashion enthusiasts who are passionate about style and creativity. Our brand is built on the foundation of inclusivity, diversity, and sustainability, and we strive to embody these values in everything we do.",
                ],
            },
            {
                'heading': 'Our Story',
                'paragraphs': [
                    'CREATE PASSION Fashion was founded with a simple yet powerful vision: to redefine the fashion industry by offering stylish, high-quality clothing and accessories that are affordable and sustainable. What started as a small online boutique has grown into a thriving fashion brand, thanks to our loyal customers who appreciate our commitment to quality and style.',
                ],
            },
            {
                'heading': 'Our Commitment to Sustainability',
                'paragraphs': [
                    'As a responsible fashion brand, we are committed to reducing our environmental impact by sourcing sustainable materials, reducing waste, and supporting ethical practices in our supply chain. We believe that fashion should not cost the earth, which is why we are constantly exploring new ways to make our products more eco-friendly.',
                ],
            },
            {
                'heading': 'Our Customer Promise',
                'paragraphs': [
                    'At CREATE PASSION Fashion, we are dedicated to providing our customers with an exceptional shopping experience. From our easy-to-use website to our friendly customer service team, we strive to make every interaction with us as seamless and enjoyable as possible. We value your feedback and are always looking for ways to improve our products and services.',
                ],
            },
            {
                'heading': 'Join Us',
                'paragraphs': [
                    "Join us on our journey to redefine fashion and make a positive impact on the world. Whether you're a trendsetter, a fashionista, or simply someone who loves great style, CREATE PASSION Fashion has something for you. Explore our collection today and discover the joy of expressing your unique style with CREATE PASSION.",
                ],
            },
            {
                'heading': 'Mission',
                'paragraphs': [
                    'Our mission is to empower individuals to express their unique style through high-quality, trendy fashion that is accessible and affordable. We aim to inspire confidence and self-expression in our customers, helping them look and feel their best every day.',
                ],
            },
            {
                'heading': 'Vision',
                'paragraphs': [
                    'Our vision is to become a globally recognized fashion brand known for our commitment to quality, innovation, and customer satisfaction. We strive to constantly evolve and adapt to changing fashion trends, ensuring that our customers always have access to the latest styles and designs.',
                ],
            },
        ],
    },
    'company-policy': {
        'title': 'Company Policy',
        'sections': [
            {
                'heading': 'Privacy Policy',
                'paragraphs': [
                    'We follow this privacy policy in accordance with applicable law. We are committed to protecting and respecting your privacy.',
                ],
                'bullets': [
                    "We don't share your personal information with anyone except for those in our business, like our corporate entities and that too with your consent only.",
                    'We store and process all your information including your precious financial information as prescribed by the Information and Technology Act, 2000 and the rules underlying in it.',
                    'If need be, details are provided only if necessary to respond to subpoenas, court orders and other legal matters.',
                    'Disclosure of your Personal Information from our end will take place only to law enforcement offices, third party rights owners, or others if necessary to implement our Terms or Privacy Policy.',
                    "If there is a violation of a third party's interests, we would have to intervene to protect the rights, property or personal safety of our users or the general public.",
                    'Our sole purpose is to provide you with a smooth, hassle-free and safe online experience, and for that, we process your Personal information very promptly.',
                ],
            },
            {
                'heading': 'Cookies Policy',
                'paragraphs': [
                    'Correspondence Information: These are a set of some basic information which you share when you become a part of our online family.',
                    'Personal Information: Just the mandatory ones like your Name, Gender, Images, Contact/Address, Phone number, email id and Nationality. Some Financial details if you are opting for online payment methods, like Credit/Debit card details including Card Number, Expiry Information, and Details for Net Banking and Wallet services.',
                    'Some Identity related Information: like AADHAR and PAN as per the prevailing government prescribed norm.',
                    'We ensure the whole information is encrypted as per the guidelines specified by Payments Cards Industry Data Security Standard (PCI DSS).',
                    'Nobody, not even the company employees, can access your personal information without authorization. We are bound by legal obligations to make sure that only the people above the age of 18 years access the server, under the Indian Contract Act 1872.',
                    'Those who are "Incompetent to Contract" by the Indian Contract Act, 1872 that include minors, undischarged insolvents etc. are not eligible to use the platform.',
                    'If you are a Minor, you are advised not to register as a User on the platform and make any transactions.',
                    'We will maintain a record of your account history including billing details and payment history. We also preserve your transaction IDs and e-commerce activities, other than Banking Details, on our secure and encrypted servers.',
                    'In case you forget your password or user IDs we got your back. We have all your usernames, passwords, email ids contact and account details with us including third-party accounts secured with us.',
                    'Any content that is provocative or threatening is strictly banned on the CREATE PASSION (OPC) PRIVATE LIMITED platform.',
                ],
            },
        ],
    },
    'terms-and-conditions': {
        'title': 'Terms and Conditions',
        'sections': [
            {
                'heading': 'Terms & Conditions (Direct Seller Agreement)',
                'paragraphs': [
                    'Definition:',
                ],
                'bullets': [
                    'Direct Seller Contract/Agreement shall mean and include the following, including amendment, modifications and re-enactment thereof: Direct seller application forms, company business plan and business manual, code of ethics for independent associate or independent distributor, 30 days return and refund policy of the company, and independent distributors license transfer policy.',
                    'The company may publish, modify and update the given policies and documents on its website.',
                    'Age of Independent Distributor: The Independent Distributor of the Company is above 18 years of age and has submitted true information and valid documents in support of his/her particulars and undertakes full responsibility for the genuineness of Identification Documents being submitted.',
                    'Distributorship / Direct Selling is subjected to the independent distributor buying the products of the company with his/her own consent and becoming the independent distributor where he/she independently grows his/her sales.',
                    'Duration: this contract shall remain valid and continue to remain in full force unless terminated by the company as mentioned in point no. 9.',
                    'Return and refund Policies: the independent distributor completely understands the return and refund policy. The independent distributor can return and refund products within 30 days of the date of invoice.',
                    'Distributorship Transfer: independent distributor can transfer his/her distributorship to his/her nominee or blood relation in case of death of the independent distributor.',
                    "Payment and Bank Accounts: Company makes all payments of incentives, discounts, refund etc. through NEFT transaction in favour of distributor's account which he/she filled in his/her profile at the time of sign up. The company never deals in cash.",
                ],
            },
            {
                'heading': 'Obligation to the Independent Distributors',
                'bullets': [
                    "Independent distributors shall not sell any company products exceeding the MRP mentioned on the labels of the company's products unless authorized by the company in writing.",
                    'Independent distributors must follow all laws, regulations and company policies.',
                    "Independent distributor shall not mislead about product information or the company's compensation plan. If found so, the company reserves its rights to take strict action.",
                    'Independent distributor shall not provide any literature or training which goes against the policies and laws of the company.',
                    'Independent distributor shall not share his/her password or login details with any third party. If he/she does so, then he/she is responsible for it.',
                    'Independent distributor shall not indulge in any kind of illegal and unethical activities. If he/she does so, strict action will be taken.',
                ],
            },
            {
                'heading': 'Termination of the Direct Seller Agreement',
                'bullets': [
                    'If independent distributor returns products within 30 days of the date of invoice and applies for the refund, then after clearing all the amount to distributor this agreement will be terminated.',
                    'If independent distributor violates the code of ethics and conduct, then company reserves the rights to terminate his/her distributorship.',
                    'If independent distributor involves in any kind of illegal activities within the company premises or is found misleading other distributors, then company reserves rights to terminate his/her distributorship with immediate effect.',
                ],
            },
            {
                'heading': 'Relationship Between Parties',
                'paragraphs': [
                    "The independent distributor hereby confirms that he/she entered into this agreement as an independent contractor. Company does not promise him/her any kind of job or employment. It is understood by the independent distributor that he/she always operates as an independent contractor, acting in his/her own name and at his/her own responsibility while purchasing products from the company. Independent Distributor earns incentives as per compensation plan from the selling of the products. Incentives solely depend upon distributor's own skill, ability and performance at sale promotion.",
                ],
            },
            {
                'heading': 'Dispute Resolution Mechanism',
                'paragraphs': [
                    'The independent distributor shall approach the grievance redressal mechanism of the company in case of any conflict or dispute with the company within 30 days from the date of events. The company will provide adequate solution within 30 days from the date of raising your concern to the company.',
                ],
            },
            {
                'heading': 'Amendment and Modification',
                'paragraphs': [
                    'The company reserves unconditional and exclusive rights to amend, modify, discontinue or introduce its business plan, policies, terms and conditions at any time without any notice or liability.',
                ],
            },
            {
                'heading': 'Disclaimer',
                'paragraphs': [
                    'I, the undersigned, hereby confirm that I have completed 18 years of my age. All the information is explained to me in my vernacular language, I am joining as Direct Seller at my own will and not forced by my sponsor or company. I will be solely responsible for any loss due to my decision to become Direct Seller with the company and I will not hold company or my sponsor guilty or responsible in whatever way in future.',
                    'I agree to adhere to and abide by the conditions mentioned hereunder. I shall become a Direct Seller on purchase of various products which will make me eligible for a relation as a Direct Seller with the Company. My Direct Seller relation cannot be transferred, sold or assigned to any person without the prior written consent of the company.',
                    'I am responsible to pay all my applicable taxes from time to time and the Company will not be held liable for the same. I have no objection and I agree to the Company deducting tax at source from my weekly/monthly actual cheque as per rates prescribed under the Income Tax Act 1961 or pay the same as prescribed under any other law for the time being in force or any modification thereof.',
                    "I solemnly confirm that the information set forth is accurate to the best of my knowledge and belief and have read, understood and hereby agree to the terms and conditions given in the reverse side of this form and those prevalent/updated on the company's website, a copy of which has been made available to me by my sponsor. I also confirm and agree to abide by such terms and conditions modified or amended by the said company from time to time.",
                    'By signing here, I expressly agree to be abiding by terms and conditions of this Contract.',
                ],
            },
        ],
    },
    'return-and-refund': {
        'title': 'Return and Refund',
        'sections': [
            {
                'heading': 'Return and Refund Policy',
                'paragraphs': [
                    'CREATE PASSION (OPC) PRIVATE LIMITED would like to thank you for being associated with us and shopping with us.',
                    'This Policy describes our consumer-friendly product cancellation, return, cooling off period, buy back and refund policy in respect of shopping made on our platforms.',
                    'Any and all claims of shopping cancellation, return, exchange, or refund shall be dealt with by this policy. The Company reserves its right to change the Policy at any time without prior notice. Please review this policy periodically.',
                ],
            },
            {
                'heading': 'Returns and Refund Policy',
                'paragraphs': [
                    'CREATE PASSION (OPC) PRIVATE LIMITED offers returns and refund policies for products that can be initiated within 30 days from the date of invoice.',
                ],
                'bullets': [
                    'Defective products.',
                    'Damage during delivery.',
                    'Missing products.',
                    'Wrong products delivered.',
                    'Customer does not want to continue the business.',
                    'Single E-pins should not be used.',
                ],
            },
            {
                'heading': 'Cooling Off Time',
                'paragraphs': [
                    'Return and refund policy is valid only up to 30 days from the date of invoice and only when E-PINS are not used.',
                ],
            },
            {
                'heading': 'Terms of Return and Refund Policy',
                'bullets': [
                    'The company has a no-question-asked return and refund policy subject to quality parameters and guidelines. Return period is 30 days from the date of invoice. No cases will be entertained after this duration.',
                    'Before accepting shipment, make sure the product package is not damaged or tampered. If the package is tampered or damaged, refuse delivery. Accepting such shipments is entirely at your own risk and the company will not be responsible.',
                    'If you are not satisfied due to defects or deficiency in the products, you may initiate an exchange, replacement or return request, or contact us through the mail given on our website.',
                    'If you want to cancel your order within 30 days of invoice, your eligible amount will be paid directly to your bank through NEFT transaction.',
                    'In case of damaged or wrong products received, you must register your complaint on our registered email id within 24 to 72 hours from the date of delivery. Claims reported after 72 hours will not be entertained.',
                    'The product claimed for return should be in proper condition with proper tagging and packing. If the product is not in proper condition, there will be no refund for that product.',
                    'All returns, replacements and refunds shall be subject to successful completion of quality check at the Company warehouse.',
                    'Refund of amount will be initiated for saleable, sealed, unopened products only, if specifically requested and upon successful completion of quality checks.',
                    'The Company will initiate your refund request within 7 working days after receiving the product at the warehouse.',
                ],
            },
            {
                'heading': 'Return Pick Up and Processing',
                'bullets': [
                    'Upon receipt of request for product return, the Company reverse-logistics partners shall get in touch with you to facilitate pickup. Only three pickup attempts will be made.',
                    'Where the Company is unable to facilitate pickup, you are required to self-ship the product to the Company warehouse and share courier or postal receipt details through customer care email or website options.',
                    'You may be reimbursed expenses incurred on self-shipment equivalent to shipping charges paid by you at the time of placing the order, subject to the conditions of this policy.',
                ],
            },
            {
                'heading': 'Claims of Non-Receipt or Delivery of Products',
                'bullets': [
                    'The company makes efforts to deliver ordered products within 10 days from the date of purchase. If delivery exceeds 10 days and you do not receive your order, contact customer care with order details.',
                    'Cases of non-receipt must be informed to customer care within 15 days from the date of purchase. Otherwise, the company will not accept any claim and the order will be considered delivered.',
                    'Subject to timely intimation, the Company shall investigate the matter with the courier partner and provide resolution such as expedited delivery, reshipment or refund, as applicable.',
                ],
            },
            {
                'heading': 'Delivery Policy',
                'bullets': [
                    'Company delivers ordered products through different courier partners and makes efforts to deliver within 10 days from the date of purchase.',
                    'Every customer receives delivery details such as tracking ID, docket number and expected delivery time on registered number and profile panel.',
                    'If customer is unable to attend calls from the delivery partner, the delivery partner will attempt delivery three more times.',
                    'If delivery partner is unable to connect even after attempts, the company will try to connect with the customer.',
                    'If the customer still does not receive the order, that order will be returned to origin at the warehouse. Customer can ask for refund of that order.',
                    'Refund will be processed according to Return and Refund Policy after deduction of delivery charges.',
                    'If after return to origin the customer wants to receive the ordered product, he/she can contact customer care.',
                    'For such orders, customer has to pay delivery charges again for receiving the same order.',
                ],
            },
        ],
    },
    'shipping-policy': {
        'title': 'Shipping Policy',
        'sections': [
            {
                'heading': 'Shipping Policy',
                'paragraphs': [
                    'Thank you for shopping at CREATE PASSION (OPC) PRIVATE LIMITED. We are committed to delivering your order accurately, in good condition, and always on time.',
                ],
            },
            {
                'heading': 'Shipping Charges',
                'paragraphs': [
                    'Shipping charges are calculated based on the weight of your order and your delivery location. The charges will be displayed at checkout before payment.',
                ],
            },
            {
                'heading': 'Shipping Time',
                'paragraphs': [
                    'We strive to process and dispatch all orders within 1-3 business days. Delivery times may vary depending on your location and selected shipping method. Once dispatched, you will receive tracking details to monitor the order progress.',
                ],
            },
            {
                'heading': 'Domestic Shipping',
                'paragraphs': [
                    'For domestic orders, we offer standard shipping and expedited shipping options. Standard shipping usually takes 3-7 business days, while expedited shipping takes 1-3 business days.',
                ],
            },
            {
                'heading': 'International Shipping',
                'paragraphs': [
                    'We may ship internationally to select countries. International shipping times vary depending on destination and method chosen. International orders may be subject to customs procedures, which can cause delays beyond original delivery estimates.',
                ],
            },
            {
                'heading': 'Shipping Restrictions',
                'paragraphs': [
                    'We are unable to ship to P.O. boxes or APO/FPO addresses. Some items may have shipping restrictions due to size, weight, or content. Please check the product page for any specific restrictions.',
                ],
            },
            {
                'heading': 'Order Tracking',
                'paragraphs': [
                    'You can track your order using the tracking number provided in the shipping confirmation message. If you have questions about your order or shipping, please contact our customer service team.',
                ],
            },
            {
                'heading': 'Why Choose CREATE PASSION Fashion for Shipping?',
                'bullets': [
                    'Reliable Delivery: We work with trusted shipping partners to ensure your order arrives on time.',
                    'Secure Packaging: Your order is packed securely to prevent damage during transit.',
                    'Convenient Tracking: Easily track your order journey from warehouse to doorstep.',
                    'Exceptional Customer Service: Our customer service team is available to assist with shipping-related queries.',
                ],
            },
        ],
    },
    'unauthorized-sales-and-false-information': {
        'title': 'Unauthorized Sales and False Information',
        'sections': [
            {
                'heading': 'Unauthorized Sales',
                'paragraphs': [
                    'It is the value and policy of CREATE PASSION (OPC) PRIVATE LIMITED to sell its products only through authorized channels. Authorized Social Sellers can only sell apparel created by CREATE PASSION (OPC) PRIVATE LIMITED.',
                    'Products created by CREATE PASSION (OPC) PRIVATE LIMITED cannot be sold on any other websites or in retail shops. The opportunity presented to distributors will diminish if products are sold through unauthorized channels. CREATE PASSION (OPC) PRIVATE LIMITED does not take responsibility for authenticity of products purchased through unauthorized channels.',
                ],
            },
            {
                'heading': 'False Information',
                'bullets': [
                    'CREATE PASSION (OPC) PRIVATE LIMITED is not involved in providing any kind of jobs and does not have any vacancies. Certain individuals may promise jobs and fixed salaries in the name of the company through social media or other sources. The Company does not recruit through these platforms.',
                    'If you want independent distributorship of our company, you can approach an authorized independent distributor nearby.',
                    'In case of misleading information or doubt, any individual can contact customer care and ask for correct information.',
                ],
            },
        ],
    },
    'disclaimer': {
        'title': 'Disclaimer',
        'sections': [
            {
                'heading': 'Disclaimer',
                'paragraphs': [
                    'I, the undersigned, hereby confirm that I have completed 18 years of age. All information is explained to me in my vernacular language. I am joining as direct seller at my own will and not forced by my sponsor or company.',
                    'I will be solely responsible for any loss due to my decision to become Direct Seller with the Company and I will not hold the Company or my sponsor guilty or responsible in any way in future.',
                    'I agree to adhere to and abide by the conditions mentioned hereunder. I shall become a Direct Seller on purchase of various products which will make me eligible for a relation as a Direct Seller with the Company.',
                    'My Direct Seller relation cannot be transferred, sold, or assigned to any person without prior written consent of the Company. I am responsible to pay all applicable taxes from time to time and the Company will not be held liable for the same.',
                    'I have no objection and agree to the Company deducting tax at source from my weekly/monthly actual cheque as per rates prescribed under the Income Tax Act 1961 or any other law for the time being in force.',
                    'I solemnly confirm that the information set forth is accurate to the best of my knowledge and belief and have read, understood and agree to the terms and conditions prevalent or updated by the Company from time to time.',
                    'By signing here, I expressly agree to be abiding by terms and conditions of this Contract.',
                ],
            },
        ],
    },
    'licience-transfer': {
        'title': 'Licience Transfer',
        'sections': [
            {
                'heading': 'License Transfer Policy',
                'paragraphs': [
                    'Independent Distributor License transfer Policy.',
                    'Death ends a life, not a relationship. This policy describes how business license benefits may be transferred to a nominee in case of unfortunate death of an Independent Distributor.',
                ],
            },
            {
                'heading': 'This Policy Will Apply If',
                'bullets': [
                    'This Policy is extended to every Independent Distributor irrespective of level in the Company. Subject to this Policy, benefits associated with the business license may be transferred to the assigned nominee in case of unfortunate death.',
                    'The entitlement of nominee for business incentives shall be decided as per the level of Independent Distributor and the business incentive plan applicable from time to time.',
                    'This is a goodwill gesture by the Company to extend financial support to the nominee. It shall not be considered an entitlement or legal right of an Independent Distributor or nominee/legal heir.',
                    'The decision of the Company shall be final and binding with respect to any claim raised under this Policy.',
                ],
            },
            {
                'heading': 'Eligibility Criteria',
                'bullets': [
                    'Person must register nominee details at the time of sign up with the Company.',
                    'All existing distributors must fill their nominee details with the Company.',
                    'Nominee details can be edited by contacting customer care of the Company.',
                    'The ID of Independent Distributor must be operational or active at the time of death, meaning the Independent Distributor made a transaction on the ID within the last 12 months before death.',
                    'Nominee should be in blood relation or spouse of the Independent Distributor.',
                    'Nominee must be above the age of 18.',
                    'Nominee must have legal documents such as Aadhar card, PAN card and proper bank details with IFSC code.',
                    'The ID should not have any active investigation going on in the Company at the time of death.',
                    'Since this benefit is extended as a goodwill gesture, the Company will not accept requests where the Independent Distributor failed to register nominee details during their lifetime.',
                ],
            },
            {
                'heading': 'Procedure of License Transfer',
                'bullets': [
                    'Nominee must inform the Company about death of the deceased ID through customer care email or customer care helpline number provided on the site.',
                    'The ID of deceased Independent Distributor will be blocked and the Company will ask for further documentation from the nominee.',
                    'Required documents include Death Certificate, self-attested AADHAR of nominee, self-attested PAN card of nominee, self-attested bank details such as cancelled cheque/passbook/bank statement, photograph of nominee and other documents as required by the Company.',
                    'Post verification of details, the Company shall execute requisite agreement with the nominee before accepting the request and transferring the existing ID to the nominee.',
                    'Post receipt of signed agreement, the ID of deceased IBO shall be mapped to the nominee and associated benefits along with future business incentives shall continue to be paid to the nominee bank account, subject to this Policy.',
                    'Payment of business incentives shall be governed by the level of Independent Distributor at the event of death and sales of products. The Company does not guarantee any kind of income.',
                ],
            },
        ],
    },
    'faq': {'title': 'Frequently Asked Questions', 'sections': [{'paragraphs': ['Content will be added soon.']}]},
}


def static_page(request, slug):
    page = PAGE_CONTENT.get(slug)
    if not page:
        raise Http404('Page not found')
    return render(request, 'static_pages/content_page.html', {'page': page, 'slug': slug})
