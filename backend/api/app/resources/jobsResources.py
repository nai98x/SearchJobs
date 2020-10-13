from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema, JobDetailsSchema
from ..database.JobModel import Job
from ..database.CompanyModel import Company
from ..database.RequirementModel import Requirement
from ..database.ApplicationModel import Application

from ..common.error_handling import ObjectNotFound, BadRequest
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json

jobs_bp = Blueprint('jobs_bp', __name__)

job_schema = JobSchema()

api = Api(jobs_bp)


class JobR(Resource):
    def get(self, id):
        j = Job.get_by_id(id)
        if j is not None:
            res = {
                'msg': 'Ok',
                'results': JobDetailsSchema().dump(j)
            }
            return make_response(jsonify(res), 200)
        raise ObjectNotFound('No existe un trabajo para el Id dado.')


class JobsSearchR(Resource):
    def post(self):
        data = request.get_json()
        if data is None:
            raise BadRequest('No se encontraron los filtros.')
        pagResult = Job.get_pag(data)
        return makePagResponse(pagResult, JobSearchResultsSchema())



        
api.add_resource(JobR, '/api/jobs/<int:id>')
api.add_resource(JobsSearchR, '/api/jobs/search')


# ADMIN ENDPOINTS

class JobsRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        for job in data:
            j = Job(job['url'], job['title'])
            j.location = job['location']
            j.workday = job['workday']
            j.contract_type = job['contract_type']
            j.salary = job['salary']
            j.description = job['description']
            j.save()
            for requirement in job['requirements']:
                j.requirements.append(Requirement(requirement))
            j.save()
            c = Company.get_by_name(job['company_name'])
            if c is not None:
                c.jobs.append(j)
                c.save()
            else:
                c = Company(job['company_name'])
                c.jobs.append(j)
                c.save()
            
        return "Ok", 201

class JobsMipleoRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        for job in data:
            j = Job(job['url'], job['title'])
            j.location = job['location']
            if job['workday'] == 'Tiempo Completo':
                j.workday = 'FullTime'
            elif job['workday'] == 'Medio Tiempo':
                j.workday = 'ParTime'
            elif job['workday'] == 'Por Horas':
                j.workday = 'ParTime'
            elif job['workday'] == 'Tiempo parcial':
                j.workday = 'ParTime'
            elif job['workday'] == 'A convenir':
                j.workday = 'NotSpecified'
            if job['contract_type'] == 'Contrato por tiempo indefinido':
                j.contract_type = 'undefined'
            elif job['contract_type'] == 'Contrato por tiempo determinado':
                j.contract_type = 'defined'
            elif job['contract_type'] == 'Contrato a Plazo Indeterminado':
                j.contract_type = 'undefined'
            else:
                j.contract_type = 'other'
            if job['salary'] == 'A convenir':
                j.salary = None
                j.salary_max = None
            else:
                s = job['salary'].split()[1].replace(',00', '').replace('.','')
                j.salary = s
                j.salary_max = s
            j.description = job['description']
            j.save()
            for requirement in job['requirements']:
                r = requirement.split(':')
                j.requirements.append(Requirement(r[0], r[1]))
            j.save()
            c = Company.get_by_name(job['company_name'])
            if c is not None:
                c.jobs.append(j)
                c.save()
            else:
                c = Company(job['company_name'])
                c.jobs.append(j)
                c.save()
            
        return "Ok"

class JobRA(Resource):
    def get(self, id):
        user_id = validateToken(request, 'funcionario')
        j = Job.get_by_id(id)
        if j is not None:
            res = {
                'msg': 'Ok',
                'results': JobSchema().dump(j)
            }
            return make_response(jsonify(res), 200)  
        raise ObjectNotFound('No existe un trabajo para el Id dado.')



api.add_resource(JobsRA, '/api/jobs/a')
api.add_resource(JobRA, '/api/jobs/a/<int:id>')