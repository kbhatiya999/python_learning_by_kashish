from sqlalchemy import Column, Integer, String, DateTime, text, VARCHAR, JSON, ForeignKey
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship

from job_match_application.database import Base


class Requirement(Base):
    __tablename__ = 'requirement'

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('user.user_id'))
    candidate = Column(VARCHAR(255))
    weight = Column(Integer)
    last_job_processed = Column(Integer)
    name = Column(String(255))
    primary_email=Column(String(50))
    linkedin_url = Column(String(255))
    preferred_location = Column(String(255))
    preferred_location_list = Column(String(255))
    preferred_location_json = Column(JSON)
    target_job_priority1 = Column(String(255))
    target_job_priority1_exp = Column(String(50))
    target_job_priority2 = Column(String(255))
    target_job_priority2_exp = Column(String(50))
    target_job_priority3 = Column(String(255))
    target_job_priority3_exp = Column(String(50))
    target_job_priority4 = Column(String(255))
    target_job_priority4_exp = Column(String(50))
    relevant_work_experience = Column(String(50))
    target_companies = Column(String(255))
    target_companies_list = Column(String(255))
    preferred_industry = Column(String)
    visa_status = Column(String(50))
    visa_details = Column(String(255))
    total_work_experience = Column(String(255))
    domain_experience = Column(String(255))
    relational = Column(String(255))
    relational_ex_type = Column(String(50))
    relational_ex_level = Column(String(50))
    relational_y = Column(String(50))
    relational_m = Column(String(50))
    non_relational = Column(String(255))
    non_relational_ex_type = Column(String(50))
    non_relational_ex_level = Column(String(50))
    non_relational_y = Column(String(50))
    non_relational_m = Column(String(50))
    tech_stack = Column(String(255))
    tech_stack_ex_type = Column(String(50))
    tech_stack_ex_level=Column(String(50))
    tech_stack_m = Column(String(50))
    tech_stack_y = Column(String(50))
    operating_system = Column(String(255))
    operating_system_ex_type = Column(String(50))
    operating_system_ex_level = Column(String(50))
    operating_system_y = Column(String(50))
    operating_system_m = Column(String(50))
    source_control_tool = Column(String(255))
    source_control_tool_ex_type = Column(String(50))
    source_control_tool_ex_level = Column(String(50))
    source_control_tool_y = Column(String(50))
    source_control_tool_m = Column(String(50))
    deployment_tool = Column(String(255))
    deployment_tool_ex_type = Column(String(50))
    deployment_tool_ex_level = Column(String(50))
    deployment_tool_y = Column(String(50))
    deployment_tool_m = Column(String(50))
    web_services = Column(String(255))
    web_services_ex_type = Column(String(50))
    web_services_ex_level = Column(String(50))
    web_services_y = Column(String(50))
    web_services_m = Column(String(50))
    api_design = Column(String(255))
    api_design_ex_type = Column(String(255))
    api_design_ex_level = Column(String(50))
    api_design_y = Column(String(50))
    api_design_m = Column(String(50))
    web_developement = Column(String(255))
    web_developement_ex_type = Column(String(50))
    web_developement_ex_level = Column(String(50))
    web_developement_m = Column(String(50))
    web_developement_y = Column(String(50))
    iOS_developement = Column(String(255))
    iOS_developement_ex_type = Column(String(50))
    iOS_developement_ex_level = Column(String(50))
    iOS_developement_y = Column(String(50))
    iOS_developement_m = Column(String(50))
    android_developement = Column(String(255))
    android_developement_ex_type = Column(String(50))
    android_developement_ex_level = Column(String(50))
    android_developement_y = Column(String(50))
    android_developement_m = Column(String(50))
    data_visualization = Column(String(255))
    data_visualization_ex_type = Column(String(50))
    data_visualization_ex_level = Column(String(50))
    data_visualization_m = Column(String(50))
    data_visualization_y = Column(String(50))
    tools = Column(String(255))
    certification = Column(String(255))
    lanaguages_skills = Column(String(255))
    extra_info = Column(String(255))
    skills_to_exclude = Column(String(255))
    industries_to_exclude = Column(String(255))
    status=Column('job_match_status', Integer)
    exp_by_admin = Column(String(255))
    created_on = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    # user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship("User")
    url_slug = Column(VARCHAR(100))
    primary_phone = Column(VARCHAR(30))
    json_data = Column(JSON)
    resume = Column(VARCHAR(255))
    json_expertise = Column(JSON)
    heading = Column(MEDIUMTEXT)
    candidate_profile = Column(VARCHAR(100))

    def __repr__(self):
        return "<Requirement(candidate_id = %d,candidate = '%s',name = '%s',linkedin_url = '%s',preferred_location = " \
               "'%s',preferred_location_list = '%s',target_job_priority1 = '%s',target_job_priority2 = '%s'," \
               "target_job_priority3 = '%s',target_job_priority4 = '%s',target_companies = '%s',target_companies_list " \
               "= '%s',preferred_industry = '%s',visa_status = '%s',visa_details = '%s',total_work_experience = '%s'," \
               "domain_experience = '%s',relational = '%s',relational_ex_type = '%s',relational_y = '%s',relational_m " \
               "= '%s',non_relational = '%s',non_relational_ex_type = '%s',non_relational_y = '%s',non_relational_m = " \
               "'%s',tech_stack = '%s',tech_stack_ex_type = '%s',tech_stack_m = '%s',tech_stack_y = '%s'," \
               "operating_system = '%s',operating_system_ex_type = '%s',operating_system_y = '%s',operating_system_m " \
               "= '%s',source_control_tool = '%s',source_control_tool_ex_type = '%s',source_control_tool_y = '%s'," \
               "source_control_tool_m = '%s',deployment_tool = '%s',deployment_tool_ex_type = '%s',deployment_tool_y " \
               "= '%s',deployment_tool_m = '%s',web_services = '%s',web_services_ex_type = '%s',web_services_y = " \
               "'%s',web_services_m = '%s',api_design = '%s',api_design_ex_type = '%s',api_design_y = '%s'," \
               "api_design_m = '%s',web_developement = '%s',web_developement_ex_type = '%s',web_developement_m = " \
               "'%s',web_developement_y = '%s',iOS_developement = '%s',iOS_developement_ex_type = '%s'," \
               "iOS_developement_y = '%s',iOS_developement_m = '%s',android_developement = '%s'," \
               "android_developement_ex_type = '%s',android_developement_y = '%s',android_developement_m = '%s'," \
               "data_visualization = '%s',data_visualization_ex_type = '%s',data_visualization_m = '%s'," \
               "data_visualization_y = '%s',tools = '%s',certification = '%s',lanaguages_skills = '%s',extra_info = " \
               "'%s',skills_to_exclude = '%s',industries_to_exclude = '%s',created_on = '%s')>" \
               % (self.candidate_id,
                  self.candidate,
                  self.name,
                  self.linkedin_url,
                  self.preferred_location, self.preferred_location_list, self.target_job_priority1,
                  self.target_job_priority2, self.target_job_priority3, self.target_job_priority4,
                  self.target_companies, self.target_companies_list, self.preferred_industry, self.visa_status,
                  self.visa_details, self.total_work_experience, self.domain_experience, self.relational,
                  self.relational_ex_type, self.relational_y, self.relational_m, self.non_relational,
                  self.non_relational_ex_type, self.non_relational_y, self.non_relational_m, self.tech_stack,
                  self.tech_stack_ex_type, self.tech_stack_m, self.tech_stack_y, self.operating_system,
                  self.operating_system_ex_type, self.operating_system_y, self.operating_system_m,
                  self.source_control_tool, self.source_control_tool_ex_type, self.source_control_tool_y,
                  self.source_control_tool_m, self.deployment_tool, self.deployment_tool_ex_type,
                  self.deployment_tool_y, self.deployment_tool_m, self.web_services, self.web_services_ex_type,
                  self.web_services_y, self.web_services_m, self.api_design, self.api_design_ex_type, self.api_design_y,
                  self.api_design_m, self.web_developement, self.web_developement_ex_type, self.web_developement_m,
                  self.web_developement_y, self.iOS_developement, self.iOS_developement_ex_type,
                  self.iOS_developement_y, self.iOS_developement_m, self.android_developement,
                  self.android_developement_ex_type, self.android_developement_y, self.android_developement_m,
                  self.data_visualization, self.data_visualization_ex_type, self.data_visualization_m,
                  self.data_visualization_y, self.tools, self.certification, self.lanaguages_skills, self.extra_info,
                  self.skills_to_exclude, self.industries_to_exclude, self.created_on)




class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    category = Column(VARCHAR(255))
    name = Column(String(121))
    email = Column(String(121))
    phone = Column(String(121))
    status = Column(TINYINT, server_default=text("'0'"))
    # otp = Column(String(121))
    password = Column(String(121))
    type = Column(TINYINT, server_default=text("'0'"))
    user_type = Column(TINYINT, server_default=text("'0'"))
    created_date = Column(DateTime, server_default=text("'1970-01-01 00:00:00'"))